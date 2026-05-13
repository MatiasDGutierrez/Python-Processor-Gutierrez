# 🚜 Agribiz Data Processor - Gutierrez

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Project Status](https://img.shields.io/badge/status-development-orange.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Solución inteligente para la normalización y consolidación de listas de precios de proveedores de maquinaria agrícola.

---

## 🌟 Visión General

Este repositorio centraliza la lógica de ingesta y transformación para catálogos y listas de precios provenientes de múltiples proveedores. Dado que cada proveedor utiliza formatos distintos (Excel, PDF, CSV), **Agribiz Data Processor** actúa como una capa de abstracción que normaliza estos datos en un esquema único y listo para el análisis de mercado.

## 🚀 Características Principales

-   **Modularidad:** Extractores específicos para `Excel`, `PDF` y `CSV`.
-   **Configuración desacoplada:** El mapeo de columnas se define en archivos YAML/JSON sin tocar el código fuente.
-   **Pipeline Robusto:** Proceso automatizado de Descubrimiento -> Extracción -> Transformación.
-   **Consistencia:** Validación automática de SKUs, precios y categorías.

## 🛠️ Stack Tecnológico

-   **Lenguaje:** Python 3.10+
-   **Procesamiento:** Pandas / Polars
-   **Extracción PDF:** Docling / PDFPlumber
-   **Configuración:** YAML / JSON

## 📂 Estructura del Proyecto

```text
├── config/             # Reglas de mapeo por proveedor
├── data-cruda/         # Archivos originales (Excel, PDF)
├── docs/               # Documentación y análisis de datos
├── output/             # Archivos normalizados finales
├── src/
│   ├── discovery/      # Análisis previo de archivos
│   ├── extractors/     # Lógica de lectura (Excel, PDF, Base)
│   └── main.py         # Punto de entrada principal
└── requirements.txt    # Dependencias del proyecto
```

## ⚙️ Instalación y Uso

### Configuración del Entorno

1. **Clonar el repositorio:**
   ```bash
   git clone <tu-repo-url>
   cd business-proyect
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

### Ejecución

Para procesar los documentos actuales en `data-cruda/`:
```bash
python src/main.py
```

---

## 📝 Notas para Colaboradores
Por favor, consulte el archivo [AGENTS.md](./AGENTS.md) para lineamientos de desarrollo y el [PRD.md](./PRD.md) para detalles sobre el alcance del producto.

---
*Desarrollado por [Pablo Chamena](https://github.com/pablochamena00)*
