# Nota Técnica: Sistema de Normalización y Exploración Multifuente

## 1. Arquitectura y Separación de Responsabilidades
El desarrollo del sistema se estructuró bajo un modelo modular para garantizar la mantenibilidad, escalabilidad y claridad del código fuente:
- **`config.py` (Reglas y Configuración):** Centraliza las reglas de negocio estáticas, incluyendo el mapeo de estados heterogéneos hacia un catálogo unificado, las tasas de conversión base hacia USD y los formatos de fecha permitidos.
- **`etl.py` (Normalización, Validación y Métricas):** Contiene la lógica principal de procesamiento. Lee el conjunto de datos de entrada, aplica validaciones rigurosas (identificando IDs ausentes, clientes vacíos, montos inválidos/negativos y fechas corruptas) y separa los registros erróneos en una estructura de auditoría aislada.
- **`app.py` (Interfaz Interactiva):** Desarrollada con Streamlit para permitir la exploración visual, filtrado dinámico por fuente y estado, visualización de métricas en tiempo real y paneles expandibles para la revisión de errores.

## 2. Criterios de Validación y Manejo de Errores
El sistema implementa una separación estricta entre registros válidos e inválidos:
- Las transacciones que no superan las validaciones estructurales no interrumpen ni colapsan el flujo del sistema; son capturadas de forma controlada y etiquetadas con su motivo de fallo específico.
- Los montos en moneda extranjera se convierten de forma automatizada aplicando factores explícitos definidos en el archivo de configuración.

## 3. Requisitos del Entorno e Instrucciones de Ejecución
Para garantizar el correcto funcionamiento del sistema, se requiere contar con Python instalado en el equipo y ejecutar los siguientes pasos en la terminal dentro de la carpeta del proyecto:

### A. Instalación de Dependencias
El sistema requiere las librerías `streamlit` para la interfaz gráfica y `pandas` para el manejo estructurado de los DataFrames y cálculos analíticos. Instálalas ejecutando:

```bash
pip install streamlit pandas
para correrlo:
python -m streamlit run app.py
