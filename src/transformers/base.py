from abc import ABC, abstractmethod
import pandas as pd

class BaseTransformer(ABC):
    """
    Clase base para todos los transformadores de datos.
    Define el contrato para convertir datos extraídos crudos en el esquema unificado.
    Esquema: [SKU, DESCRIPCION, PRECIO, MONEDA, PROVEEDOR]
    """

    def __init__(self, provider_config: dict):
        self.config = provider_config
        self.target_columns = ["SKU", "DESCRIPCION", "PRECIO", "MONEDA", "PROVEEDOR"]

    @abstractmethod
    def transform(self, raw_data) -> pd.DataFrame:
        """
        Transforma los datos crudos al esquema unificado.
        """
        pass

    def clean_price(self, price_str) -> float:
        """
        Lógica común para normalizar strings de precios a float.
        Maneja formatos: 1.234,56 | 1,234.56 | 1.234 | 1,234
        """
        if pd.isna(price_str) or price_str == "":
            return 0.0
        
        if isinstance(price_str, (int, float)):
            return float(price_str)
            
        # Eliminar símbolos de moneda, letras y espacios
        # Conservar solo dígitos, puntos y comas
        price_str = str(price_str).replace("$", "").replace(" ", "").strip()
        # Eliminar cualquier carácter que no sea dígito, punto o coma
        import re
        price_str = re.sub(r'[^\d.,]', '', price_str)
        
        if not price_str:
            return 0.0
            
        # Caso 1: Tiene puntos y comas
        if "," in price_str and "." in price_str:
            last_dot = price_str.rfind(".")
            last_comma = price_str.rfind(",")
            if last_dot < last_comma:
                # Caso: 1.234,56 -> 1234.56
                price_str = price_str.replace(".", "").replace(",", ".")
            else:
                # Caso: 1,234.56 -> 1234.56
                price_str = price_str.replace(",", "")
        
        # Caso 2: Solo tiene comas
        elif "," in price_str:
            if price_str.count(",") == 1:
                pos = price_str.rfind(",")
                # Si hay 2 dígitos después de la coma, es decimal
                if len(price_str) - pos <= 3:
                    price_str = price_str.replace(",", ".")
                else:
                    # Probablemente separador de miles (ej: 1,000)
                    price_str = price_str.replace(",", "")
            else:
                # Múltiples comas -> todas son miles
                price_str = price_str.replace(",", "")
                
        # Caso 3: Solo tiene puntos
        elif "." in price_str:
            if price_str.count(".") == 1:
                pos = price_str.rfind(".")
                remaining = len(price_str) - pos - 1
                if remaining == 3:
                    # Caso: 1.234 -> 1234
                    price_str = price_str.replace(".", "")
                elif remaining == 5:
                    # Caso detectado en fragmentación PDF: 1.23400 (era 1.234,00)
                    price_str = price_str.replace(".", "")
                    price_str = price_str[:-2] + "." + price_str[-2:]
                elif remaining > 3:
                    # Otros casos con muchos decimales o miles mal puestos
                    price_str = price_str.replace(".", "")
                else:
                    # Es decimal (ej: 123.45 o 1.2)
                    pass
            else:
                # Múltiples puntos -> todos son miles
                price_str = price_str.replace(".", "")
                
        try:
            return float(price_str)
        except ValueError:
            return 0.0

    def validate_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Asegura que el DataFrame resultante tenga exactamente las columnas requeridas.
        """
        # Asegurar que existan todas las columnas
        for col in self.target_columns:
            if col not in df.columns:
                df[col] = None
        
        return df[self.target_columns]
