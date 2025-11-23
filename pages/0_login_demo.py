# pages/0_login_demo.py
import streamlit as st
from auth import show_login_streamlit

user = show_login_streamlit()
if user:
    st.write("Bienvenido:", user)
    st.info("Usa la barra lateral para navegar entre páginas CRUD.")
else:
    st.info("Por favor inicia sesión para continuar.")
