# Guía de Trabajo para Agentes y Colaboradores

Para trabajar en este repositorio y asegurar que el procesamiento de datos se realice correctamente, se debe configurar y activar el entorno de Python siguiendo estos pasos:

## 1. Configuración del Entorno de Python
Es fundamental usar un entorno virtual para mantener las dependencias aisladas y evitar conflictos.

### Crear el entorno virtual:
Ejecuta el siguiente comando en la raíz del proyecto:
```bash
python3 -m venv venv
```

### Activar el entorno virtual:
Antes de realizar cualquier tarea o instalación, activa el entorno:
```bash
source venv/bin/activate
```

### Instalar dependencias:
Con el entorno activado, instala las librerías necesarias:
```bash
pip install -r requirements.txt
```

## 2. Ejecución de Scripts
Para procesar los documentos de los proveedores, utiliza el script principal (una vez que esté desarrollado):
```bash
python src/main.py
```

## 3. Notas para Agentes (AI)
Al trabajar en este repositorio, siempre asegúrate de:
1.  Verificar que el entorno virtual esté activo si vas a realizar pruebas de ejecución.
2.  Respetar la estructura de carpetas definida en el `PRD.md`.
3.  Documentar cualquier cambio en la lógica de mapeo de proveedores en la carpeta `config/`.

## 4. Uso de Context7 MCP
Este proyecto recomienda el uso del MCP de **Context7** para obtener información técnica siempre actualizada y precisa.

### Habilitación del MCP:
Para habilitar esta herramienta, el agente debe asegurarse de que la configuración correspondiente esté activa en el archivo de configuración global:
`~/.gemini/settings.json` (agregando la clave necesaria para habilitar el servidor MCP de Context7).

### Cuándo utilizarlo:
Es obligatorio que el agente emplee el MCP de Context7 en los siguientes casos:
1.  **Contexto Actualizado:** Cuando se requiera información precisa sobre cómo emplear una herramienta, librería o software (ej. nuevas funcionalidades de Pandas, mejores prácticas de extracción con pdfplumber, etc.).
2.  **Documentación Técnica:** Cuando se necesiten datos actualizados referidos a desarrollo de software o derivados que se encuentren disponibles en Context7.
3.  **Migraciones y Versiones:** Para verificar cambios entre versiones de librerías (ej. la transición de PyPDF2 a pypdf) y evitar el uso de métodos obsoletos.

El uso de este MCP garantiza que las soluciones propuestas sigan los estándares más recientes de la industria.

## 5. Orquestación de Agentes Subordinados
Para optimizar la eficiencia y el uso de contexto, el agente principal debe orquestar agentes especializados cuando la complejidad de la tarea lo requiera.

### Cuándo invocar al `codebase_investigator`:
*   **Análisis Arquitectónico:** Antes de realizar cambios estructurales o refactorizaciones profundas.
*   **Mapeo de Dependencias:** Para entender el impacto sistémico de un cambio en un módulo específico.
*   **Investigación de Causa Raíz:** Cuando un error requiera rastrear el flujo de datos a través de múltiples capas del sistema.
*   **Clarificación de Requerimientos:** Ante peticiones vagas que requieran un plan de acción basado en la estructura actual del proyecto.

### Cuándo invocar al `generalist`:
*   **Tareas de Alto Volumen:** Refactorizaciones repetitivas en múltiples archivos o limpieza de deuda técnica extensiva.
*   **Gestión de Contexto:** Para ejecutar procesos que requieran muchos pasos intermedios, evitando saturar la memoria de la sesión principal.
*   **Ejecución de Pruebas y Logs:** Para analizar salidas extensas de comandos o logs sin comprometer la legibilidad del historial principal.

### Cuándo invocar al `arquitect`:
*   **Investigación Técnica:** Búsqueda de documentación actualizada y análisis de nuevas librerías (ej. Docling) mediante Context7.
*   **Diseño de Soluciones:** Propuestas de cambios estructurales basadas en investigación externa y local.

### Cuándo invocar al `refactorer`:
*   **Mejora de Código:** Limpieza, aplicación de patrones de diseño y optimización de lógica existente.
*   **Migraciones Técnicas:** Transición controlada entre versiones de librerías manteniendo la estabilidad funcional.


### Protocolo de Actuación:
1.  **Evaluación Inicial:** Determinar si la tarea se beneficia de la especialización de un subagente.
2.  **Instrucción Precisa:** Definir claramente el objetivo y los límites de la tarea delegada.
3.  **Síntesis de Resultados:** Integrar los hallazgos del subagente en la sesión principal de forma estructurada y accionable.
