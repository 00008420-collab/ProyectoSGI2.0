import streamlit as st
from crud_full import get_all, get_by_id, create, update, delete, get_columns

TABLE = "Grupo"
ID_COL = "Id_grupo"

st.title("Grupos — CRUD")
cols = get_columns(TABLE)
st.write("Columnas:", cols)

with st.expander("Listar grupos"):
    st.dataframe(get_all(TABLE, limit=300))

st.subheader("Crear grupo")
with st.form("create_grupo"):
    inputs = {}
    for c in cols:
        if c == ID_COL:
            continue
        inputs[c] = st.text_input(c, "")
    submit = st.form_submit_button("Crear")
    if submit:
        try:
            new = create(TABLE, inputs)
            st.success(f"Grupo creado (Id: {new})")
        except Exception as e:
            st.error(e)

st.subheader("Buscar / Actualizar / Eliminar")
buscar = st.text_input("Id grupo", "")
if st.button("Cargar grupo"):
    rec = get_by_id(TABLE, ID_COL, buscar)
    if not rec:
        st.info("No encontrado")
    else:
        st.json(rec)
        with st.form("update_grupo"):
            upd = {}
            for c in cols:
                if c == ID_COL:
                    st.text_input(c, value=str(rec.get(c)), disabled=True)
                else:
                    upd[c] = st.text_input(c, value=str(rec.get(c) or ""))
            ok = st.form_submit_button("Actualizar")
            if ok:
                try:
                    update(TABLE, ID_COL, buscar, upd)
                    st.success("Actualizado")
                except Exception as e:
                    st.error(e)
        if st.button("Eliminar grupo"):
            try:
                delete(TABLE, ID_COL, buscar)
                st.success("Eliminado")
            except Exception as e:
                st.error(e)
