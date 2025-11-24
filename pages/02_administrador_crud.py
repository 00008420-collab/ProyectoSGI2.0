import streamlit as st
from crud_full import get_all, get_by_id, create, update, delete, get_columns

TABLE = "administrador"
ID_COL = "id_administrador"

st.title("Administrador — CRUD")
cols = get_columns(TABLE)
if not cols:
    st.warning(f"No se detectan columnas para la tabla '{TABLE}'.")
else:
    st.write("Columnas detectadas:", cols)

with st.expander("Listar administradores"):
    try:
        rows = get_all(TABLE, limit=500)
        st.write(f"{len(rows)} registros encontrados")
        st.dataframe(rows)
    except Exception as e:
        st.error(e)

st.markdown("---")
st.subheader("Crear administrador")
with st.form("create_administrador"):
    inputs = {}
    for c in cols:
        if c == ID_COL:
            continue
        inputs[c] = st.text_input(c)
    if st.form_submit_button("Crear"):
        try:
            new_id = create(TABLE, inputs)
            st.success(f"Administrador creado (id: {new_id})")
        except Exception as e:
            st.error(e)

st.markdown("---")
st.subheader("Buscar / Actualizar / Eliminar")
buscar = st.text_input("Id administrador", "")
if st.button("Cargar administrador"):
    rec = get_by_id(TABLE, ID_COL, buscar)
    if not rec:
        st.info("No encontrado")
    else:
        st.json(rec)
        with st.form("update_administrador"):
            upd = {}
            for c in cols:
                if c == ID_COL:
                    st.text_input(c, value=str(rec.get(c)), disabled=True)
                else:
                    upd[c] = st.text_input(c, value=str(rec.get(c) or ""))
            if st.form_submit_button("Actualizar"):
                try:
                    update(TABLE, ID_COL, buscar, upd)
                    st.success("Actualizado")
                except Exception as e:
                    st.error(e)
        if st.button("Eliminar administrador"):
            try:
                delete(TABLE, ID_COL, buscar)
                st.success("Eliminado")
            except Exception as e:
                st.error(e)
