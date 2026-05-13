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
