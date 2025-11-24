import streamlit as st
from crud_full import get_all, get_by_id, create, update, delete, get_columns

TABLE = "asistencia"
ID_COL = "id_asistencia"

st.title("Asistencia — CRUD")
cols = get_columns(TABLE)
if not cols:
    st.warning(f"No se detectan columnas para la tabla '{TABLE}'.")
else:
    st.write("Columnas detectadas:", cols)

with st.expander("Listar asistencias"):
    try:
        rows = get_all(TABLE, limit=500)
        st.write(f"{len(rows)} registros encontrados")
        st.dataframe(rows)
    except Exception as e:
        st.error(e)

st.markdown("---")
st.subheader("Registrar asistencia")
with st.form("create_asistencia"):
    inputs = {}
    for c in cols:
        if c == ID_COL:
            continue
        if "fecha" in c.lower():
            inputs[c] = st.date_input(c)
        else:
            inputs[c] = st.text_input(c)
    if st.form_submit_button("Registrar"):
        payload = {k: (v.isoformat() if hasattr(v,"isoformat") else v) for k,v in inputs.items()}
        try:
            new = create(TABLE, payload)
            st.success(f"Asistencia registrada (id: {new})")
        except Exception as e:
            st.error(e)

st.markdown("---")
st.subheader("Buscar / Editar / Eliminar")
buscar = st.text_input("Id asistencia", "")
if st.button("Cargar asistencia"):
    rec = get_by_id(TABLE, ID_COL, buscar)
    if not rec:
        st.info("No encontrado")
    else:
        st.json(rec)
        with st.form("update_asistencia"):
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
        if st.button("Eliminar asistencia"):
            try:
                delete(TABLE, ID_COL, buscar)
                st.success("Eliminado")
            except Exception as e:
                st.error(e)
