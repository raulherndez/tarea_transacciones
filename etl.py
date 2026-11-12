"""
etl.py
Módulo de Normalización, Validación y Cálculo de Métricas.
"""
import json
import pandas as pd
from datetime import datetime
from config import MAPEO_ESTADOS, TASAS_CAMBIO, FORMATOS_FECHA

class ProcesadorETL:
    def __init__(self, ruta_json):
        self.ruta_json = ruta_json
        self.raw_data = []
        self.df_validas = pd.DataFrame()
        self.df_invalidas = pd.DataFrame()

    def cargar_datos(self):
        """Lee transacciones desde el archivo JSON de entrada."""
        with open(self.ruta_json, 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)

    def _normalizar_fecha(self, fecha_bruta):
        if not fecha_bruta:
            return None
        for fmt in FORMATOS_FECHA:
            try:
                return datetime.strptime(str(fecha_bruta).strip(), fmt).strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                continue
        try:
            return pd.to_datetime(fecha_bruta).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return None

    def ejecutar_proceso(self):
        self.cargar_datos()
        validas = []
        invalidas = []

        for item in self.raw_data:
            motivos_error = []

            # 1. Validación de ID
            tx_id = item.get("transaction_id") or item.get("id")
            if not tx_id or str(tx_id).strip() == "":
                motivos_error.append("ID de transacción ausente")

            # 2. Validación de Cliente
            cliente = item.get("client_name") or item.get("cliente")
            if not cliente or str(cliente).strip() == "":
                motivos_error.append("Cliente ausente")

            # 3. Validación de Monto
            monto_bruto = item.get("amount") or item.get("monto")
            try:
                monto = float(monto_bruto)
                if monto <= 0:
                    motivos_error.append("Monto menor o igual a cero")
            except:
                motivos_error.append("Monto no numérico / inválido")
                monto = 0.0

            # 4. Validación de Fecha
            fecha_bruta = item.get("date") or item.get("fecha")
            fecha_norm = self._normalizar_fecha(fecha_bruta)
            if not fecha_norm:
                motivos_error.append("Formato de fecha inválido")

            # Criterio de descarte o separación
            if motivos_error:
                item_inv = item.copy()
                item_inv["motivo_falla"] = ", ".join(motivos_error)
                invalidas.append(item_inv)
            else:
                # Transformación y Normalización
                moneda = (item.get("currency") or item.get("moneda") or "USD").upper()
                tasa = TASAS_CAMBIO.get(moneda, 1.0)
                monto_usd = round(monto * tasa, 2)

                estado_bruto = (item.get("status") or item.get("estado") or "COMPLETADA").upper()
                estado_norm = MAPEO_ESTADOS.get(estado_bruto, "PENDIENTE")

                validas.append({
                    "id_transaccion": tx_id,
                    "fuente_origen": item.get("source_system", item.get("origen", "EXTERNA")),
                    "fecha": fecha_norm,
                    "cliente": str(cliente).strip().title(),
                    "monto_usd": monto_usd,
                    "moneda_original": moneda,
                    "estado": estado_norm
                })

        self.df_validas = pd.DataFrame(validas)
        self.df_invalidas = pd.DataFrame(invalidas)
        return self.df_validas, self.df_invalidas

    def obtener_metricas(self):
        """Genera las métricas requeridas."""
        total_proc = len(self.raw_data)
        total_val = len(self.df_validas)
        total_inv = len(self.df_invalidas)
        monto_total = self.df_validas['monto_usd'].sum() if not self.df_validas.empty else 0.0
        
        conteo_estados = self.df_validas['estado'].value_counts().to_dict() if not self.df_validas.empty else {}
        conteo_monedas = self.df_validas.groupby('moneda_original')['monto_usd'].agg(['count', 'sum']).to_dict(orient='index') if not self.df_validas.empty else {}

        return {
            "total_procesadas": total_proc,
            "total_validas": total_val,
            "total_invalidas": total_inv,
            "monto_total_usd": monto_total,
            "porcentaje_exito": (total_val / total_proc * 100) if total_proc > 0 else 0,
            "conteo_estados": conteo_estados,
            "conteo_monedas": conteo_monedas
        }