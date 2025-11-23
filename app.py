# app.py
import streamlit as st
from modulos.venta import mostrar_venta
from modulos.login import login

# Comprobamos si la sesión ya está iniciada 
if "sesion_iniciada" in st.session_state and st.session_state["sesion_iniciada"]:

    # Botón de logout en el menú lateral
    if st.sidebar.button("Cerrar sesión"):
        st.session_state["sesion_iniciada"] = False
        st.rerun()  # ← Nueva forma de recargar la app

    # Mostrar el menú lateral
    opciones = ["Ventas", "Otra opción"]
    seleccion = st.sidebar.selectbox("Selecciona una opción", opciones)

    # Contenido según la opción
    if seleccion == "Ventas":
        mostrar_venta()
    elif seleccion == "Otra opción":
        st.write("Has seleccionado otra opción.")

else:
    # Si la sesión no está iniciada, mostrar el login
    login()
