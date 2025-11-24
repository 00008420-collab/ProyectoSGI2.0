# app.py
"""
App principal Streamlit (simple viewer de tablas).
- Muestra login si existe auth.show_login_streamlit
- Lista tablas detectadas y permite ver registros (SELECT * LIMIT 200)
- Permanece ligero y seguro: usa db.get_table_names_safe y get_session_local
- Asegúrate de configurar Secrets en Streamlit Cloud (DB_* variables)
"""

import streamlit as st
import os

st.set_page_config(page_title="GAPC - Data Explorer", layout="wide")

st.title("GAPC — Explorador de Base de Datos (demo)")

# Mostrar enlace al PDF del proyecto (ruta local subida en este entorno)
st.markdown("**Documentación del proyecto:** `/mnt/data/Proyecto final rev.pdf`")

# Intentar usar modulo auth si existe (no obligatorio)
user = None
try:
    from auth import show_login_streamlit

    user = show_login_streamlit()
except Exception:
    # si no hay auth, no interrumpimos la app
    pass

if user is None:
    if "auth_user" in st.session_state and st.session_state.get("auth_user"):
        user = st.session_state.get("auth_user")

if user:
    st.sidebar.success(f"Autenticado: {user}")
else:
    st.sidebar.info("Sin autenticación (modo demo)")

# Importar funciones de db (seguro: no conecta hasta que se usan)
from db import get_table_names_safe, get_session_local, get_table_columns

st.sidebar.header("Conexión y diagnóstico")
ok, msg = True, ""
try:
    ok_conn, msg = False, ""
    # test de conexión ligero
    from db import test_connection

    ok_conn, msg = test_connection()
except Exception:
    ok_conn, msg = False, "No se pudo ejecutar test_connection()"

if ok_conn:
    st.sidebar.success("DB: Conexión OK")
else:
    st.sidebar.error(f"DB: error - {msg}")

# Mostrar tablas detectadas
tables = get_table_names_safe()
st.subheader("Tablas detectadas en la base de datos")
if not tables:
    st.warning("No se detectaron tablas. Revisa Secrets o la conexión a la base de datos.")
else:
    st.write(", ".join(tables))

# Selección segura de tabla
selected = st.selectbox("Selecciona una tabla para ver (solo lectura)", options=[""] + tables)
if selected:
    cols = get_table_columns(selected)
    st.write("Columnas:", cols)
    # Mostrar registros (límite configurable)
    limit = st.number_input("Límite de filas a mostrar", min_value=10, max_value=1000, value=200, step=10)
    if st.button("Cargar registros"):
        try:
            SessionLocal = get_session_local()
            session = SessionLocal()
            try:
                safe_sql = f"SELECT * FROM `{selected}` LIMIT :lim"
                res = session.execute(safe_sql, {"lim": int(limit)})
                rows = res.fetchall()
                keys = res.keys()
                # convertir a lista de dicts
                data = [dict(zip(keys, r)) for r in rows]
                st.dataframe(data)
                st.success(f"{len(data)} filas cargadas desde `{selected}`")
            finally:
                session.close()
        except Exception as e:
            st.error(f"Error al cargar registros: {e}")

# Footer - info de entorno (no mostrar valores secretos)
st.markdown("---")
st.caption("Recuerda: configura tus Secrets en Streamlit Cloud: DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME.")
