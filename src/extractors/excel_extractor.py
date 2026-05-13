import pandas as pd
from .base import BaseExtractor

class ExcelExtractor(BaseExtractor):
    def extract(self) -> pd.DataFrame:
        try:
            # Intentamos leer el archivo. Pandas maneja .xls y .xlsx si las librerías están instaladas.
            df = pd.read_excel(self.file_path)
            return df
        except Exception as e:
            print(f"Error extrayendo Excel {self.file_path}: {e}")
            return pd.DataFrame()
