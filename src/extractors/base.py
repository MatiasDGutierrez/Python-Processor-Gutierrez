from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict

class BaseExtractor(ABC):
    """
    Clase base para todos los extractores de datos de proveedores.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """
        Método que debe ser implementado por cada extractor para obtener un DataFrame.
        """
        pass

    def preview(self, n_rows: int = 5):
        """
        Muestra una vista previa de los datos extraídos.
        """
        df = self.extract()
        print(f"\nVista previa de {self.file_path}:")
        print(df.head(n_rows))
        return df
