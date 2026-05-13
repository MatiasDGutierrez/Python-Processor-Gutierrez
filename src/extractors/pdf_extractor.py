import pdfplumber
import pandas as pd
from .base import BaseExtractor

class PDFExtractor(BaseExtractor):
    def extract(self) -> pd.DataFrame:
        all_data = []
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    # Extraer tablas de la página
                    tables = page.extract_tables()
                    for table in tables:
                        # Cada tabla es una lista de listas
                        all_data.extend(table)
            
            if not all_data:
                return pd.DataFrame()
                
            df = pd.DataFrame(all_data)
            return df
        except Exception as e:
            print(f"Error extrayendo PDF {self.file_path}: {e}")
            return pd.DataFrame()

    def extract_words(self) -> pd.DataFrame:
        """
        Extrae todas las palabras del PDF con sus coordenadas espaciales.
        Retorna un DataFrame con [text, x0, top, x1, bottom, page]
        """
        all_words = []
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    words = page.extract_words()
                    for word in words:
                        word['page'] = i + 1
                        all_words.append(word)
            
            return pd.DataFrame(all_words)
        except Exception as e:
            print(f"Error extrayendo palabras del PDF {self.file_path}: {e}")
            return pd.DataFrame()
