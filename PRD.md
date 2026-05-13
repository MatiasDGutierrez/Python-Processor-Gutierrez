# Product Requirement Document (PRD) - Procesador de Datos de Maquinaria Agrícola

## 1. Visión General del Proyecto
Este proyecto está dedicado al procesamiento de datos entregados por proveedores de maquinaria agrícola. La finalidad de este repositorio es procesar los documentos que envían los proveedores, cada uno con su lista de precios en un formato distinto, centralizando y normalizando la información para su posterior uso.

## 2. Objetivos Principales
*   **Normalización de Formatos:** Implementar un sistema capaz de interpretar diversos formatos de archivos (Excel, CSV, PDF, etc.) provenientes de distintos proveedores.
*   **Procesamiento Automatizado:** Reducir la carga manual de limpieza y carga de datos.
*   **Consistencia de Datos:** Asegurar que la información extraída (SKUs, precios, descripciones, categorías) siga un estándar unificado.
*   **Trazabilidad:** Mantener un registro de qué datos provienen de qué proveedor y cuándo fueron actualizados.

## 3. Alcance del Sistema
*   **Ingesta:** Lectura de archivos desde directorios locales (ej. `data-cruda/`) o fuentes externas.
*   **Transformación:** Aplicación de reglas de negocio específicas por proveedor para mapear columnas a un esquema común.
*   **Validación:** Verificación de integridad de datos (precios numéricos, existencia de SKUs).
*   **Salida:** Generación de un archivo normalizado o inserción en una base de datos central.

## 4. Requisitos Técnicos (Preliminar)
*   **Lenguaje:** Python (recomendado por su ecosistema de procesamiento de datos como Pandas/Polars).
*   **Manejo de Archivos:** Soporte para `.xlsx`, `.xls`, `.csv`.
*   **Configuración:** Uso de archivos de configuración (JSON/YAML) para definir los mapeos por proveedor sin necesidad de cambiar el código base.

## 5. Estructura de Directorios (Propuesta)
*   `data-cruda/`: Carpeta para los archivos originales de los proveedores.
*   `src/`: Código fuente del procesador.
*   `config/`: Definiciones de mapeo por cada proveedor.
*   `output/`: Datos procesados y normalizados.
