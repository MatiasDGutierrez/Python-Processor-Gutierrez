import os
import pandas as pd
from pathlib import Path

def crear_excel_unificado():
    """
    Lee todos los CSV normalizados del directorio output/ y crea un Excel unificado
    con una columna PROVEEDOR para identificar rápidamente el origen de los datos.
    """
    output_dir = "output"
    
    if not os.path.exists(output_dir):
        print(f"Error: No se encuentra el directorio '{output_dir}'")
        return
    
    # Obtener todos los archivos CSV
    csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"No se encontraron archivos CSV en '{output_dir}'")
        return
    
    print(f"Procesando {len(csv_files)} archivos CSV...")
    
    all_dataframes = []
    
    for csv_file in csv_files:
        csv_path = os.path.join(output_dir, csv_file)
        
        try:
            # Leer el CSV
            df = pd.read_csv(csv_path)
            
            # Extraer el proveedor del nombre del CSV
            # El formato es: normalized_{PROVEEDOR}_{NOMBRE_ARCHIVO}.csv
            if csv_file.startswith("normalized_"):
                nombre_sin_prefijo = csv_file[len("normalized_"):-4]
                partes = nombre_sin_prefijo.split("_", 1)
                proveedor = partes[0] if len(partes) > 0 else "DESCONOCIDO"
            else:
                proveedor = "DESCONOCIDO"
            
            # Extraer el nombre del archivo original
            if len(partes) > 1:
                archivo_original = partes[1]
            else:
                archivo_original = nombre_sin_prefijo
            
            # Agregar columnas de identificación al inicio
            # Verificar si la columna PROVEEDOR ya existe
            if 'PROVEEDOR' not in df.columns:
                df.insert(0, 'PROVEEDOR', proveedor)
            
            # Agregar ARCHIVO_ORIGINAL si no existe
            if 'ARCHIVO_ORIGINAL' not in df.columns:
                df.insert(1, 'ARCHIVO_ORIGINAL', archivo_original)
            
            all_dataframes.append(df)
            print(f"✓ {csv_file}: {len(df)} filas, proveedor: {proveedor}")
            
        except Exception as e:
            print(f"✗ Error procesando {csv_file}: {e}")
    
    if not all_dataframes:
        print("No se pudo procesar ningún archivo.")
        return
    
    # Combinar todos los dataframes
    df_unificado = pd.concat(all_dataframes, ignore_index=True)
    
    # Guardar como Excel
    output_excel = os.path.join(output_dir, "inventario_unificado.xlsx")
    df_unificado.to_excel(output_excel, index=False, sheet_name='Inventario')
    
    print(f"\n✓ Excel unificado creado: {output_excel}")
    print(f"  Total de filas: {len(df_unificado)}")
    print(f"  Total de columnas: {len(df_unificado.columns)}")
    print(f"  Proveedores: {df_unificado['PROVEEDOR'].unique().tolist()}")

if __name__ == "__main__":
    crear_excel_unificado()
