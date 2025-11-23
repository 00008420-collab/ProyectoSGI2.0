# app.py
import streamlit as st
from db import get_table_names_safe
from auth import show_login_streamlit

st.set_page_config(page_title="GAPC - Sistema", layout="wide")
st.title("GAPC — Sistema de Gestión")

# Login simple
user = show_login_streamlit()
if not user:
    st.stop()

# App principal
st.sidebar.title("Navegación")
pages = ["Inicio", "Miembros", "Grupos", "Préstamos", "Pagos", "Multas y Reuniones", "Módulo avanzado"]
choice = st.sidebar.selectbox("Ir a", pages)

if choice == "Inicio":
    st.header("Inicio — Resumen")
    st.markdown("Tablas detectadas en la base de datos:")
    tablas = get_table_names_safe()
    st.write(tablas)

else:
    st.markdown(f"Ve a la barra lateral → `pages/` para abrir los módulos CRUD específicos.")
    st.info("Las páginas CRUD están disponibles en la carpeta `pages/` y Streamlit las mostrará automáticamente.")
