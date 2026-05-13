import os
import yaml
import pandas as pd
from discovery.analyzer import FileAnalyzer
from extractors.excel_extractor import ExcelExtractor
from extractors.pdf_extractor import PDFExtractor
from transformers.factory import TransformerFactory

def load_config(config_path="config/providers.yaml"):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def detect_provider(filename, config):
    """
    Intenta detectar el proveedor basándose en el nombre del archivo.
    """
    providers = config.get("providers", {}).keys()
    filename_upper = filename.upper()
    for provider in providers:
        if provider in filename_upper:
            return provider
    return None

def main():
    print("--- Procesador de Datos de Maquinaria Agrícola ---")
    
    # 0. Cargar configuración
    try:
        config = load_config()
        print("[0] Configuración de proveedores cargada.")
    except Exception as e:
        print(f"Error al cargar configuración: {e}")
        return

    raw_data_dir = "data-cruda"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(raw_data_dir):
        print(f"Error: No se encuentra el directorio '{raw_data_dir}'")
        return

    analyzer = FileAnalyzer(raw_data_dir)
    print(f"\n[1] Analizando archivos en: {raw_data_dir}...")
    analysis_results = analyzer.analyze_all()
    
    for item in analysis_results:
        filename = item['filename']
        file_path = os.path.join(raw_data_dir, filename)
        file_type = item['type']
        
        print(f"\n" + "="*50)
        print(f"Procesando: {filename} ({file_type})")
        
        # 1. Detectar proveedor
        provider_name = detect_provider(filename, config)
        if not provider_name:
            print(f"No se pudo identificar el proveedor para el archivo: {filename}. Saltando.")
            continue
        
        print(f"Proveedor detectado: {provider_name}")

        # 2. Extraer datos (Raw)
        extractor = None
        if file_type == "Excel/Structured":
            extractor = ExcelExtractor(file_path)
        elif file_type == "PDF":
            extractor = PDFExtractor(file_path)
        
        if not extractor:
            print(f"No hay un extractor implementado para el tipo: {file_type}")
            continue

        try:
            # 3. Determinar tipo de transformación y extraer datos
            provider_config = config.get("providers", {}).get(provider_name, {})
            transformer_type = provider_config.get("type", "generic")
            
            if transformer_type == "layout" and isinstance(extractor, PDFExtractor):
                print("Usando extracción por coordenadas (Layout Mode)...")
                raw_df = extractor.extract_words()
            else:
                raw_df = extractor.extract()
                
            print(f"Extracción cruda exitosa. Filas: {len(raw_df)}")
            
            # 4. Transformar datos (Normalización)
            transformer = TransformerFactory.get_transformer(provider_name, config)
            normalized_df = transformer.transform(raw_df)
            
            print(f"Transformación exitosa. Filas normalizadas: {len(normalized_df)}")
            
            if not normalized_df.empty:
                print("\nVista previa de datos normalizados:")
                print(normalized_df.head(5))
                
                # 4. Exportar
                output_filename = f"normalized_{provider_name}_{os.path.splitext(filename)[0]}.csv"
                output_path = os.path.join(output_dir, output_filename)
                normalized_df.to_csv(output_path, index=False)
                print(f"\nArchivo guardado en: {output_path}")
            else:
                print("Advertencia: El resultado de la transformación está vacío.")
                
        except Exception as e:
            print(f"Error procesando {filename}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
