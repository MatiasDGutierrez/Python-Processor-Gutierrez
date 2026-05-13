from .generic_transformer import GenericTransformer
from .layout_transformer import LayoutTransformer

class TransformerFactory:
    @staticmethod
    def get_transformer(provider_name: str, providers_config: dict):
        config = providers_config.get("providers", {}).get(provider_name)
        if not config:
            raise ValueError(f"No se encontró configuración para el proveedor: {provider_name}")
            
        transformer_type = config.get("type", "generic")
        
        if transformer_type == "generic":
            return GenericTransformer(config)
        elif transformer_type == "layout":
            return LayoutTransformer(config)
        else:
            raise NotImplementedError(f"Tipo de transformador '{transformer_type}' no implementado.")
