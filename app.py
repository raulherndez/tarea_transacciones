"""
app.py
Interfaz interactiva para la exploración de transacciones normalizadas.
Ejecutar con: streamlit run app.py
"""
import streamlit as st
import pandas as pd
from etl import ProcesadorETL

st.set_page_config(page_title="Explorador de Transacciones", page_icon="💳", layout="wide")

st.title("💳 Sistema de Exploración y Normalización de Transacciones Multifuente")
st.markdown("Interfaz interactiva para filtrado, auditoría de errores y análisis de métricas.")

# Cargar y procesar datos
@st.cache_data
def cargar_procesamiento():
    etl = ProcesadorETL("transacciones_prueba.json")
    etl.ejecutar_proceso()
    return etl.df_validas, etl.df_invalidas, etl.obtener_metricas()

try:
    df_validas, df_invalidas, metricas = cargar_procesamiento()
except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo 'transacciones_prueba.json'. Asegúrate de crearlo en la misma carpeta.")
    st.stop()

# --- PANEL DE MÉTRICAS ---
st.subheader("📊 Métricas Generales del Sistema")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Procesadas", metricas["total_procesadas"])
col2.metric("Válidas", metricas["total_validas"], delta=f"{metricas['porcentaje_exito']:.1f}%")
col3.metric("Inválidas / Descartadas", metricas["total_invalidas"], delta=f"-{100 - metricas['porcentaje_exito']:.1f}%", delta_color="inverse")
col4.metric("Monto Total (USD)", f"${metricas['monto_total_usd']:,.2f}")

st.markdown("---")

# --- FILTROS EN BARRA LATERAL ---
st.sidebar.header("🔍 Filtros de Exploración")
fuentes_disponibles = ["Todas"] + list(df_validas['fuente_origen'].unique()) if not df_validas.empty else ["Todas"]
estados_disponibles = ["Todos"] + list(df_validas['estado'].unique()) if not df_validas.empty else ["Todos"]

fuente_sel = st.sidebar.selectbox("Filtrar por Fuente", fuentes_disponibles)
estado_sel = st.sidebar.selectbox("Filtrar por Estado", estados_disponibles)

# Aplicar filtros
df_filtrado = df_validas.copy()
if fuente_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado['fuente_origen'] == fuente_sel]
if estado_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado['estado'] == estado_sel]

# --- VISUALIZACIÓN DE DATOS VÁLIDOS ---
st.subheader(f"✅ Transacciones Válidas ({len(df_filtrado)} registros mostrados)")
if not df_filtrado.empty:
    st.dataframe(df_filtrado, use_container_width=True)
else:
    st.info("No hay registros que coincidan con los filtros aplicados.")

# --- SECCIÓN DE AUDITORÍA (INVÁLIDAS) ---
with st.expander(f"⚠️ Ver Transacciones Inválidas y Motivos de Descarte ({len(df_invalidas)})"):
    st.markdown("Registros separados por no cumplir con las reglas de integridad o formato:")
    if not df_invalidas.empty:
        st.dataframe(df_invalidas, use_container_width=True)
    else:
        st.success("No hay transacciones inválidas en el conjunto de datos.")

# --- RESUMEN ADICIONAL DE MÉTRICAS ---
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    st.subheader("📌 Conteo por Estado")
    if metricas["conteo_estados"]:
        st.table(pd.DataFrame(list(metricas["conteo_estados"].items()), columns=["Estado", "Cantidad"]))
    else:
        st.write("Sin datos.")
with c2:
    st.subheader("💰 Resumen por Moneda Original")
    if metricas["conteo_monedas"]:
        tabla_monedas = []
        for mon, vals in metricas["conteo_monedas"].items():
            tabla_monedas.append({"Moneda": mon, "Transacciones": vals["count"], "Total USD": vals["sum"]})
        st.table(pd.DataFrame(tabla_monedas))
    else:
        st.write("Sin datos.")