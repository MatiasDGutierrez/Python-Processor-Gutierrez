# Investigación de Datos de Proveedores

Este documento registra los hallazgos y desafíos encontrados al analizar los archivos de precios de los proveedores de maquinaria agrícola.

## Estado Inicial (Mayo 2026)

Se han identificado 9 archivos iniciales en `data-cruda/` con los siguientes perfiles:

### 1. Archivos Excel Estructurados
- **Proveedores:** BERTINI, ARAG.
- **Formatos:** `.xls` y `.xlsx`.
- **Observaciones:** Son los más sencillos de procesar. Sin embargo, la estructura de columnas varía. Por ejemplo, BERTINI tiene una columna inicial sin nombre (`Unnamed: 0`).
- **Estrategia:** Uso de `pandas` con mapeo de columnas flexible por proveedor.

### 2. PDFs Generados Digitalmente (Clean PDFs)
- **Proveedores:** ROTAR, OH GARCIA (algunos).
- **Software detectado:** Microsoft Excel 2016, Crystal Reports.
- **Observaciones:** Contienen tablas de texto reales. Se pueden extraer coordenadas y celdas sin necesidad de OCR.
- **Estrategia:** Uso de `pdfplumber` para extraer tablas manteniendo la relación espacial de las celdas.

### 3. PDFs de Diseño/Complejos
- **Proveedores:** OH GARCIA (Transmisión).
- **Software detectado:** CorelDRAW X5.
- **Observaciones:** Al ser herramientas de diseño vectorial, el orden del texto en el archivo PDF interno puede no coincidir con el orden de lectura visual (el texto puede estar "flotando"). 
- **Estrategia:** Análisis de Layout (geometría) y posiblemente OCR de apoyo para asegurar que los precios se asocien al SKU correcto.

## Matriz de Riesgos y Desafíos
| Desafío | Impacto | Mitigación |
| :--- | :--- | :--- |
| Cambio de columnas | Alto | Archivos de configuración YAML por proveedor. |
| Texto en PDFs vectoriales | Medio | Uso de extracción por coordenadas espaciales. |
| Formatos antiguos (.xls) | Bajo | Librería `xlrd` integrada. |
| Unidades de medida/Moneda | Medio | Pipeline de normalización post-extracción. |

## Análisis Profundo de Sondas (Probes)

Para determinar la mejor estrategia, hemos sometido a los archivos a distintas "sondas" de extracción.

### Caso A: El PDF "Digitalmente Nativo" (`ROTAR 74.pdf`)
*   **Sonda de Texto Plano:** 
    ```text
    "5 - 649$ 39.610,00"
    ```
    *Dificultad:* El pegado del precio al código ocurre aleatoriamente dependiendo de la fuente.
*   **Sonda de Tabla (CSV):**
    ```csv
    CODIGO,DESCRIPCION,PRECIO
    5-649,,$ 39.610.00
    ```
    *Dificultad:* La descripción a veces está vacía o se desborda a la siguiente línea.
*   **Sonda JSON (Estructurada):**
    ```json
    {"sku": "5-649", "price": 39610.00, "currency": "ARS"}
    ```
*   **Conclusión:** La geometría es estable. No se requiere IA, solo un parser de coordenadas.

### Caso B: El PDF de Diseño (`OH GARCIA - Transmision.pdf`)
*   **Sonda de Texto Plano:** El texto aparece en un orden que no sigue la lectura humana. Fragmentos de palabras como "Engranaje" y "Z=20" pueden aparecer separados por 100 líneas de otros datos.
*   **Sonda de Tabla:** Falla. `pdfplumber` no detecta líneas de tabla porque son bordes dibujados como vectores, no como tablas reales de sistema.
*   **Sonda Visual (Layout Analysis):** 
    - Se detectan bloques de texto mediante su "bounding box" (caja delimitadora).
    - El precio siempre se encuentra en el 20% derecho de la página.
*   **Conclusión:** Este archivo requiere un **Analizador de Layout**. Debemos agrupar el texto por su proximidad física (Y-coordinate) antes de intentar darle sentido semántico.

### Caso C: El Excel de Alta Densidad (`BERTINI 10-2025.xlsx`)
*   **Sonda de Estructura:** 
    - Filas 1-8: Logos y avisos legales.
    - Fila 9: Encabezados reales.
*   **Conclusión:** Necesitamos una regla de "Búsqueda de Ancla". El script debe buscar la palabra "DESCRIPCION" o "PRECIO" en cualquier celda para determinar dónde empieza la verdadera tabla.

## Fase de Implementación: Ciclo 1 (Mayo 2026)

Se ha completado la implementación de la capa de transformación base y el procesamiento de los primeros proveedores mediante estructuras tabulares.

### Arquitectura de Transformación
Se diseñó un sistema modular basado en:
- **`BaseTransformer`**: Define el esquema unificado `[SKU, DESCRIPCION, PRECIO, MONEDA, PROVEEDOR]` y provee utilidades de limpieza de precios (manejo de formatos regionales `$ 1.234,56`).
- **`GenericTransformer`**: Implementa la lógica de "Búsqueda de Ancla" y mapeo dinámico de columnas.
- **`TransformerFactory`**: Orquestador que instancia el transformador correcto según la configuración del proveedor.

### Hallazgos de la Implementación (Generic Pipeline)
1. **Robustez de Anclas:**
   - La búsqueda de encabezados se volvió insensible a mayúsculas, acentos (normalización NFD) y espacios en blanco.
   - **Caso BERTINI:** El ancla cambió de "CODIGO" a "Código", lo que requería normalización para ser detectado consistentemente.
2. **Normalización de Precios:**
   - Se implementó un algoritmo que detecta el separador decimal vs. miles basándose en la posición relativa de puntos y comas.
3. **Configuración vs. Código:**
   - Toda la lógica específica se movió a `config/providers.yaml`, permitiendo dar de alta nuevos proveedores tabulares en minutos.

### Resultados de Validación
- **ROTAR (PDF):** Extracción exitosa de 46 ítems con descripciones multilínea.
- **BERTINI (Excel):** Extracción exitosa de 298 ítems, detectando el ancla en la fila 10 y descartando filas vacías/ilegales.
- **MG (Excel):** Se confirmó que el archivo analizado es un índice comercial sin precios. El sistema lo ignora correctamente al no encontrar el ancla definida.

