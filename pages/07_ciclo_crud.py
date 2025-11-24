import streamlit as st
from crud_full import get_all, get_by_id, create, update, delete, get_columns

TABLE = "ciclo"
ID_COL = "id_ciclo"

st.title("Ciclo — CRUD")
cols = get_columns(TABLE)
if not cols:
    st.warning(f"No se detectan columnas para la tabla '{TABLE}'.")
else:
    st.write("Columnas detectadas:", cols)

with st.expander("Listar ciclos"):
    try:
        rows = get_all(TABLE, limit=500)
        st.write(f"{len(rows)} registros encontrados")
        st.dataframe(rows)
    except Exception as e:
        st.error(e)

st.markdown("---")
st.subheader("Crear/Registrar ciclo")
with st.form("create_ciclo"):
    inputs = {}
    for c in cols:
        if c == ID_COL:
            continue
        if "fecha" in c.lower():
            inputs[c] = st.date_input(c)
        else:
            inputs[c] = st.text_input(c)
    if st.form_submit_button("Crear"):
        payload = {k: (v.isoformat() if hasattr(v,"isoformat") else v) for k,v in inputs.items()}
        try:
            new = create(TABLE, payload)
            st.success(f"Ciclo creado (id: {new})")
        except Exception as e:
            st.error(e)

st.markdown("---")
st.subheader("Buscar / Editar / Eliminar")
buscar = st.text_input("Id ciclo", "")
if st.button("Cargar ciclo"):
    rec = get_by_id(TABLE, ID_COL, buscar)
    if not rec:
        st.info("No encontrado")
    else:
        st.json(rec)
        with st.form("update_ciclo"):
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
        if st.button("Eliminar ciclo"):
            try:
                delete(TABLE, ID_COL, buscar)
                st.success("Eliminado")
            except Exception as e:
                st.error(e)
