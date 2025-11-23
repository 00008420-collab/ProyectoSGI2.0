# app.py
import streamlit as st
from db import get_table_names
st.set_page_config(page_title='GAPC - Sistema', layout='wide')
st.title('GAPC — Sistema de Gestión')

menu = ["Inicio", "Ayuda"]
choice = st.sidebar.selectbox("Menú", menu)

if choice == "Inicio":
    st.header("Resumen")
    try:
        tablas = get_table_names()
        st.write("Tablas detectadas en la base de datos:", tablas)
    except Exception as e:
        st.error("No se pudo conectar a la base de datos.")
        st.text(str(e))

elif choice == "Ayuda":
    st.header("Instrucciones rápidas")
    st.markdown("""
1. Crea un servicio MySQL en Clever Cloud e importa tus tablas.
2. Sube este proyecto a GitHub.
3. En Streamlit Cloud crea una app conectando tu repo.
4. Agrega los secrets (DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME).
""")
    st.markdown("El ZIP y el PDF del proyecto pueden subirse al repo si necesitas documentación.")

