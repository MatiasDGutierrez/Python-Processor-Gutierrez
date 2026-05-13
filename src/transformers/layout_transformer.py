import pandas as pd
from .base import BaseTransformer

class LayoutTransformer(BaseTransformer):
    """
    Transformador para PDFs con diseño complejo/vectorial.
    Reconstruye filas basándose en la proximidad geométrica de las palabras.
    """
    def transform(self, word_data: pd.DataFrame) -> pd.DataFrame:
        """
        Transforma una lista de palabras con coordenadas en filas estructuradas.
        word_data debe tener columnas: [text, x0, top, x1, bottom, page]
        """
        if word_data.empty:
            return pd.DataFrame(columns=self.target_columns)

        params = self.config.get("params", {})
        y_threshold = params.get("y_threshold", 2)
        price_x_min = params.get("price_x_min", 450)
        sku_x_max = params.get("sku_x_max", 150)

        rows = []
        # Agrupar por página
        for page_num, page_df in word_data.groupby('page'):
            # Ordenar por top (coordenada Y)
            page_df = page_df.sort_values(by=['top', 'x0'])
            
            if page_df.empty:
                continue

            current_row_y = page_df.iloc[0]['top']
            current_row_words = []
            
            for _, word in page_df.iterrows():
                # Si la palabra está en la misma 'línea' visual (dentro del umbral)
                if abs(word['top'] - current_row_y) <= y_threshold:
                    current_row_words.append(word)
                else:
                    # Procesar fila acumulada
                    processed_row = self._process_row(current_row_words, price_x_min, sku_x_max)
                    if processed_row:
                        rows.append(processed_row)
                    
                    # Iniciar nueva fila
                    current_row_y = word['top']
                    current_row_words = [word]
            
            # Procesar última fila de la página
            processed_row = self._process_row(current_row_words, price_x_min, sku_x_max)
            if processed_row:
                rows.append(processed_row)

        df = pd.DataFrame(rows)
        
        if df.empty:
            return pd.DataFrame(columns=self.target_columns)

        # Aplicar valores por defecto y limpieza
        defaults = self.config.get("defaults", {})
        df["PROVEEDOR"] = defaults.get("PROVEEDOR", "UNKNOWN")
        df["MONEDA"] = defaults.get("MONEDA", "USD")
        df["PRECIO"] = df["PRECIO"].apply(self.clean_price)
        
        # Eliminar filas donde el SKU y Precio estén vacíos (ruido de headers/logos)
        df = df[~((df["SKU"] == "") & (df["PRECIO"] == 0))]
        
        return self.validate_schema(df)

    def _process_row(self, words, price_x_min, sku_x_max):
        """
        Identifica SKU, Descripción y Precio basándose en coordenadas X.
        """
        if not words:
            return None
            
        # Las palabras ya vienen ordenadas por x0 debido al sort previo
        sku_parts = []
        desc_parts = []
        price_parts = []
        
        for w in words:
            text = str(w['text']).strip()
            if not text: continue
            
            # Clasificar por posición X
            if w['x0'] >= price_x_min:
                price_parts.append(text)
            elif w['x1'] <= sku_x_max:
                sku_parts.append(text)
            else:
                desc_parts.append(text)
                    
        sku = " ".join(sku_parts).strip()
        desc = " ".join(desc_parts).strip()
        price = "".join(price_parts).strip()

        # Si no hay nada útil, descartar
        if not sku and not price:
            return None
            
        return {
            "SKU": sku,
            "DESCRIPCION": desc,
            "PRECIO": price
        }
