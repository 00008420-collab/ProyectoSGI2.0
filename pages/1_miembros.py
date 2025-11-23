import streamlit as st
from crud_full import get_all, get_by_id, create, update, delete, get_columns

TABLE = "Miembro"
ID_COL = "Id_miembro"

st.title("Miembros — CRUD")
cols = get_columns(TABLE)
st.write("Columnas detectadas:", cols)

with st.expander("Listar miembros"):
    rows = get_all(TABLE, limit=200)
    st.write(f"{len(rows)} registros encontrados")
    st.dataframe(rows)

st.subheader("Crear nuevo miembro")
with st.form("create_miembro"):
    inputs = {}
    for c in cols:
        if c == ID_COL:
            continue
        inputs[c] = st.text_input(f"{c}", "")
    submitted = st.form_submit_button("Crear")
    if submitted:
        try:
            new_id = create(TABLE, inputs)
            st.success(f"Miembro creado (Id: {new_id})")
        except Exception as e:
            st.error(f"Error al crear miembro: {e}")

st.markdown("---")
st.subheader("Buscar / Actualizar / Eliminar miembro por ID")
buscar_id = st.text_input("Id a buscar", "")
if st.button("Cargar registro"):
    if buscar_id.strip() == "":
        st.warning("Ingresa un Id válido")
    else:
        rec = get_by_id(TABLE, ID_COL, buscar_id)
        if not rec:
            st.info("No se encontró el registro")
        else:
            st.json(rec)
            with st.form("update_miembro"):
                updated = {}
                for c in cols:
                    if c == ID_COL:
                        st.text_input(c, value=str(rec.get(c)), disabled=True)
                    else:
                        updated[c] = st.text_input(c, value=str(rec.get(c) or ""))
                ok = st.form_submit_button("Actualizar")
                if ok:
                    try:
                        update(TABLE, ID_COL, buscar_id, updated)
                        st.success("Registro actualizado")
                    except Exception as e:
                        st.error(f"Error al actualizar: {e}")

            if st.button("Eliminar registro"):
                try:
                    cnt = delete(TABLE, ID_COL, buscar_id)
                    if cnt:
                        st.success("Registro eliminado")
                    else:
                        st.info("No se eliminó nada (revisa el Id).")
                except Exception as e:
                    st.error(f"Error al eliminar: {e}")
