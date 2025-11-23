import streamlit as st
from crud import listar_tabla

st.title("Miembros — Gestión rápida")

tabla = st.text_input("Tabla:", "Miembro")
if st.button("Listar"):
    try:
        df = listar_tabla(tabla)
        st.dataframe(df)
    except Exception as e:
        st.error(e)
