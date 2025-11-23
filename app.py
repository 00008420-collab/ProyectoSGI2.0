# app.py
import streamlit as st
from db import get_table_names
from crud import listar_tabla

st.set_page_config(page_title='GAPC - Sistema', layout='wide')
st.title('GAPC — Sistema de Gestión')

menu = ["Inicio", "Miembros", "Grupos", "Préstamos", "Ayuda"]
choice = st.sidebar.selectbox("Menú", menu)

if choice == "Inicio":
    st.header("Resumen")
    try:
        tablas = get_table_names()
        st.write("Tablas detectadas en la base de datos:", tablas)
    except Exception as e:
        st.error("No se pudo conectar a la base de datos.")
        st.text(str(e))

elif choice == "Miembros":
    st.header("Miembros")
    tabla = st.text_input("Nombre de la tabla de miembros (ej: Miembro)", "Miembro")
    if st.button("Cargar miembros"):
        try:
            df = listar_tabla(tabla)
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error al cargar miembros: {e}")

elif choice == "Grupos":
    st.header("Grupos")
    tabla = st.text_input("Nombre de la tabla de grupos (ej: Grupo)", "Grupo")
    if st.button("Cargar grupos"):
        try:
            df = listar_tabla(tabla)
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error: {e}")

elif choice == "Préstamos":
    st.header("Préstamos")
    tabla = st.text_input("Nombre de la tabla de préstamos (ej: Prestamo)", "Prestamo")
    if st.button("Cargar préstamos"):
        try:
            df = listar_tabla(tabla)
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error: {e}")

elif choice == "Ayuda":
    st.header("Instrucciones rápidas")
    st.markdown("""
1. Crea un servicio MySQL en Clever Cloud e importa tus tablas.
2. Sube este proyecto a GitHub.
3. En Streamlit Cloud crea una app conectando tu repo.
4. Agrega los secrets (DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME).
""")
    st.markdown("El PDF del proyecto debe subirse al repositorio si lo deseas incluir.")
