✦ La investigación y el diseño del pipeline han sido completados por el sub-agente. A continuación, presento el resumen ejecutivo de la
  arquitectura propuesta y los hallazgos clave:

  Resumen del Diseño de Ingeniería

   1. Arquitectura de Transformers (src/transformers/):
       * BaseTransformer: Clase abstracta que define el contrato de salida: un DataFrame con el esquema [SKU, DESCRIPCION, PRECIO,
         MONEDA, PROVEEDOR].
       * GenericTransformer: Para proveedores con estructuras tabulares (Excel/PDF nativos). Utilizará un sistema de "Anclas" definido
         en configuración para detectar el inicio de la tabla y mapear columnas.
       * LayoutTransformer: Para PDFs complejos (vectoriales/CorelDRAW). Implementará lógica de reconstrucción geométrica, agrupando
         fragmentos de texto por coordenadas (proximidad en Y, alineación en X).

   2. Extracción de Datos:
       * Se identificó que los extractores actuales deben simplificarse para entregar datos "crudos":
           * ExcelExtractor: Devolverá el DataFrame sin procesar encabezados.
           * PDFExtractor: Se le añadirá el método extract_words para obtener la lista de palabras con sus coordenadas exactas,
             alimentando al LayoutTransformer.

   3. Configuración Centrada en el Proveedor (config/providers.yaml):
       * Toda la lógica específica (nombres de columnas, moneda por defecto, coordenadas de anclaje) se extraerá del código y se
         colocará en este archivo YAML, permitiendo escalar el sistema sin modificar la lógica core.

   4. Validación y Normalización:
       * Se incluirá un paso de limpieza de precios para manejar formatos regionales (puntos/comas) y conversión de moneda.

  Próximos Pasos Sugeridos
   * Implementar la estructura base en src/transformers/.
   * Crear el archivo config/providers.yaml con el primer proveedor de prueba.
   * Actualizar src/main.py para orquestar el flujo completo: Descubrimiento → Extracción Cruda → Transformación → Resultado
     Normalizado.

  ¿Deseas que proceda con la implementación de estos componentes o prefieres ajustar algún detalle del diseño?


  Topic: Completed investigation and design phase. Waiting for implementation directive.


✦ /home/pablo/Programacion/personal/business-proyect/
  ├───.gitignore
  ├───AGENTS.md
  ├───GEMINI.md
  ├───PRD.md
  ├───requirements.txt
  ├───.git/...
  ├───config/
  ├───data-cruda/...
  ├───docs/
  │   └───data_investigation.md
  ├───output/...
  ├───src/
  │   ├───__init__.py
  │   ├───main.py
  │   ├───discovery/
  │   │   ├───__init__.py
  │   │   ├───analyzer.py
  │   │   └───__pycache__/...
  │   ├───extractors/
  │   │   ├───__init__.py
  │   │   ├───base.py
  │   │   ├───excel_extractor.py
  │   │   ├───pdf_extractor.py
  │   │   └───__pycache__/...
  │   ├───transformers/
  │   │   └───__init__.py
  │   └───utils/
  │       └───__init__.py
  └───venv/...
  La investigación y el diseño del pipeline han sido completados por el sub-agente. A continuación, presento el resumen ejecutivo de la
  arquitectura propuesta y los hallazgos clave:

  Resumen del Diseño de Ingeniería

   1. Arquitectura de Transformers (src/transformers/):
       * BaseTransformer: Clase abstracta que define el contrato de salida: un DataFrame con el esquema [SKU, DESCRIPCION, PRECIO,
         MONEDA, PROVEEDOR].
       * GenericTransformer: Para proveedores con estructuras tabulares (Excel/PDF nativos). Utilizará un sistema de "Anclas" definido
         en configuración para detectar el inicio de la tabla y mapear columnas.
       * LayoutTransformer: Para PDFs complejos (vectoriales/CorelDRAW). Implementará lógica de reconstrucción geométrica, agrupando
         fragmentos de texto por coordenadas (proximidad en Y, alineación en X).

   2. Extracción de Datos:
       * Se identificó que los extractores actuales deben simplificarse para entregar datos "crudos":
           * ExcelExtractor: Devolverá el DataFrame sin procesar encabezados.
           * PDFExtractor: Se le añadirá el método extract_words para obtener la lista de palabras con sus coordenadas exactas,
             alimentando al LayoutTransformer.

   3. Configuración Centrada en el Proveedor (config/providers.yaml):
       * Toda la lógica específica (nombres de columnas, moneda por defecto, coordenadas de anclaje) se extraerá del código y se
         colocará en este archivo YAML, permitiendo escalar el sistema sin modificar la lógica core.

   4. Validación y Normalización:
       * Se incluirá un paso de limpieza de precios para manejar formatos regionales (puntos/comas) y conversión de moneda.

  Próximos Pasos Sugeridos
   * Implementar la estructura base en src/transformers/.
   * Crear el archivo config/providers.yaml con el primer proveedor de prueba.
   * Actualizar src/main.py para orquestar el flujo completo: Descubrimiento → Extracción Cruda → Transformación → Resultado
     Normalizado.

  ¿Deseas que proceda con la implementación de estos componentes o prefieres ajustar algún detalle del diseño?
