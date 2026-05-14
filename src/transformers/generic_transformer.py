import pandas as pd
import unicodedata
from .base import BaseTransformer

class GenericTransformer(BaseTransformer):
    """
    Transformador para estructuras tabulares estándar.
    Utiliza un ancla para encontrar el inicio de la tabla y mapea columnas según la configuración.
    """

    def _normalize_text(self, text):
        if pd.isna(text): return ""
        text = str(text)
        # Normalizar para quitar acentos y convertir a minúsculas
        return "".join(c for c in unicodedata.normalize('NFD', text)
                      if unicodedata.category(c) != 'Mn').lower().strip()

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df is None or df.empty:
            return pd.DataFrame(columns=self.target_columns)

        # 1. Encontrar la fila del ancla (encabezado)
        anchor_config = self.config.get("anchor")
        header_idx = self._find_header_row(df, anchor_config)
        
        # 2. Re-estructurar el DataFrame desde el encabezado
        if anchor_config and header_idx is not None:
            # Si hay ancla y se encontró, usar esa fila como encabezado
            header_row = df.iloc[header_idx].astype(str).tolist()
            df.columns = [self._normalize_text(c) for c in header_row]
            df = df.iloc[header_idx + 1:].reset_index(drop=True)
        else:
            # Si no hay ancla o no se encontró, usar las columnas originales
            df.columns = [self._normalize_text(c) for c in df.columns]
        
        # 3. Mapear columnas
        mapping = self.config.get("mapping", {})
        transformed_data = pd.DataFrame()
        
        for target_col, source_col in mapping.items():
            norm_source = self._normalize_text(source_col)
            if norm_source in df.columns:
                transformed_data[target_col] = df[norm_source]
            else:
                transformed_data[target_col] = None

        # 4. Aplicar valores por defecto
        defaults = self.config.get("defaults", {})
        for col, value in defaults.items():
            if col not in transformed_data.columns or transformed_data[col].isnull().all():
                transformed_data[col] = value

        # 5. Limpieza específica
        if "PRECIO" in transformed_data.columns:
            transformed_data["PRECIO"] = transformed_data["PRECIO"].apply(self.clean_price)
            
        # 6. Eliminar filas donde el SKU o el PRECIO sean inválidos
        transformed_data = transformed_data.dropna(subset=["SKU"])
        # Filtramos filas con precio 0 o SKU vacío después de normalizar
        transformed_data = transformed_data[transformed_data["SKU"].astype(str).str.strip() != ""]
        transformed_data = transformed_data[transformed_data["PRECIO"] > 0]

        return self.validate_schema(transformed_data)

    def _find_header_row(self, df: pd.DataFrame, anchor_config: dict):
        if not anchor_config:
            return 0
            
        pattern = self._normalize_text(anchor_config.get("pattern"))
        col_idx = anchor_config.get("column")
        
        # Buscar el patrón en la columna especificada (o en todo el df si col_idx es None)
        if col_idx is not None:
            column_data = df.iloc[:, col_idx].apply(self._normalize_text)
            matches = column_data[column_data.str.contains(pattern, na=False)]
        else:
            # Búsqueda global en las primeras 20 filas
            for i in range(min(20, len(df))):
                row_text = " ".join(df.iloc[i].apply(self._normalize_text))
                if pattern in row_text:
                    return i
            return None
            
        if not matches.empty:
            return matches.index[0]
            
        return None
