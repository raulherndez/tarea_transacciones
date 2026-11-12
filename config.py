"""
config.py
Archivo de configuración y reglas de negocio explícitas.
Definido por el estudiante para gobernar la normalización y validación.
"""

# Mapeo estricto de estados heterogéneos a un catálogo común
MAPEO_ESTADOS = {
    "COMPLETED": "COMPLETADA",
    "SUCCESS": "COMPLETADA",
    "SUCCESSFUL": "COMPLETADA",
    "APROBADA": "COMPLETADA",
    "COMPLETADA": "COMPLETADA",
    
    "PENDING": "PENDIENTE",
    "EN_ESPERA": "PENDIENTE",
    "PENDIENTE": "PENDIENTE",
    
    "FAILED": "FALLIDA",
    "RECHAZADA": "FALLIDA",
    "CANCELLED": "FALLIDA",
    "FALLIDA": "FALLIDA"
}

# Tasas de conversión base a USD
TASAS_CAMBIO = {
    "USD": 1.0,
    "EUR": 1.08,  # 1 EUR = 1.08 USD
    "CRC": 0.0019,
    "GTQ": 0.13
}

# Formatos de fecha permitidos para el parser flexible
FORMATOS_FECHA = [
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d',
    '%d/%m/%Y %H:%M',
    '%d-%m-%Y',
    '%Y/%m/%d'
]