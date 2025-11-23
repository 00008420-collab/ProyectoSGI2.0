# pages/3_prestamos_crud.py
import streamlit as st
from crud_full import get_all, get_by_id, create, update, delete, get_columns

TABLE = "Prestamo"
ID_COL = "Id_prestamo"

st.title("Préstamos — CRUD")
cols = get_columns(TABLE)
st.write("Columnas:", cols)

with st.expander("Listado de préstamos"):
    st.dataframe(get_all(TABLE, limit=300))

st.subheader("Crear préstamo")
with st.form("create_prestamo"):
    data = {}
    for c in cols:
        if c == ID_COL:
            continue
        data[c] = st.text_input(c, "")
    ok = st.form_submit_button("Crear préstamo")
    if ok:
        try:
            new = create(TABLE, data)
            st.success(f"Préstamo creado (Id: {new})")
        except Exception as e:
            st.error(e)

st.subheader("Buscar / Actualizar / Eliminar por Id")
pid = st.text_input("Id préstamo", "")
if st.button("Cargar préstamo"):
    rec = get_by_id(TABLE, ID_COL, pid)
    if not rec:
        st.info("No encontrado")
    else:
        st.json(rec)
        with st.form("update_prestamo"):
            upd = {}
            for c in cols:
                if c == ID_COL:
                    st.text_input(c, value=str(rec.get(c)), disabled=True)
                else:
                    upd[c] = st.text_input(c, value=str(rec.get(c) or ""))
            uok = st.form_submit_button("Actualizar")
            if uok:
                try:
                    update(TABLE, ID_COL, pid, upd)
                    st.success("Actualizado")
                except Exception as e:
                    st.error(e)
        if st.button("Eliminar préstamo"):
            try:
                delete(TABLE, ID_COL, pid)
                st.success("Eliminado")
            except Exception as e:
                st.error(e)
