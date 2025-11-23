# pages/5_multas_reuniones_crud.py
import streamlit as st
from crud_full import get_all, create, get_by_id, update, delete, get_columns

# Multa
TABLE_M = "Multa"
ID_M = "Id_multa"

st.header("Multas")
st.write("Columnas Multa:", get_columns(TABLE_M))
with st.expander("Listar multas"):
    st.dataframe(get_all(TABLE_M))
with st.form("crear_multa"):
    data = {}
    for c in get_columns(TABLE_M):
        if c == ID_M:
            continue
        data[c] = st.text_input(c, "")
    if st.form_submit_button("Crear multa"):
        try:
            create(TABLE_M, data)
            st.success("Multa creada")
        except Exception as e:
            st.error(e)

# Reunión
st.header("Reuniones")
TABLE_R = "Reunion"
ID_R = "Id_reunion"
st.write("Columnas Reunión:", get_columns(TABLE_R))
with st.expander("Listar reuniones"):
    st.dataframe(get_all(TABLE_R))
with st.form("crear_reunion"):
    data = {}
    for c in get_columns(TABLE_R):
        if c == ID_R:
            continue
        data[c] = st.text_input(c, "")
    if st.form_submit_button("Crear reunión"):
        try:
            create(TABLE_R, data)
            st.success("Reunión creada")
        except Exception as e:
            st.error(e)
