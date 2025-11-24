import streamlit as st
from crud_full import get_all, get_by_id, create, update, delete, get_columns

TABLE = "acta"
ID_COL = "id_acta"

st.title("Acta — CRUD")
cols = get_columns(TABLE)
if not cols:
    st.warning(f"No se detectan columnas para la tabla '{TABLE}'. Revisa el nombre en la BD.")
else:
    st.write("Columnas detectadas:", cols)

with st.expander("Listar actas"):
    try:
        rows = get_all(TABLE, limit=500)
        st.write(f"{len(rows)} registros encontrados")
        st.dataframe(rows)
    except Exception as e:
        st.error(f"Error al listar actas: {e}")

st.markdown("---")
st.subheader("Crear nueva acta")
with st.form("create_acta"):
    inputs = {}
    for c in cols:
        if c == ID_COL:
            continue
        if "fecha" in c.lower():
            inputs[c] = st.date_input(label=c)
        else:
            inputs[c] = st.text_input(label=c)
    submitted = st.form_submit_button("Crear acta")
    if submitted:
        payload = {}
        for k, v in inputs.items():
            if hasattr(v, "isoformat"):
                payload[k] = v.isoformat()
            else:
                payload[k] = v
        try:
            new_id = create(TABLE, payload)
            st.success(f"Acta creada (id: {new_id})")
        except Exception as e:
            st.error(f"Error al crear acta: {e}")

st.markdown("---")
st.subheader("Buscar / Editar / Eliminar por id_acta")
buscar_id = st.text_input("Id_acta a buscar", "")
if st.button("Cargar acta"):
    if not buscar_id.strip():
        st.warning("Ingresa un id_acta válido.")
    else:
        rec = get_by_id(TABLE, ID_COL, buscar_id)
        if not rec:
            st.info("No se encontró ese registro.")
        else:
            st.json(rec)
            with st.form("update_acta"):
                updated = {}
                for c in cols:
                    if c == ID_COL:
                        st.text_input(c, value=str(rec.get(c)), disabled=True)
                    else:
                        updated[c] = st.text_input(c, value=str(rec.get(c) or ""))
                ok = st.form_submit_button("Actualizar acta")
                if ok:
                    try:
                        update(TABLE, ID_COL, buscar_id, updated)
                        st.success("Acta actualizada.")
                    except Exception as e:
                        st.error(f"Error al actualizar: {e}")

            if st.button("Eliminar acta"):
                try:
                    cnt = delete(TABLE, ID_COL, buscar_id)
                    if cnt:
                        st.success("Acta eliminada.")
                    else:
                        st.info("No se eliminó ningún registro (revisa el id).")
                except Exception as e:
                    st.error(f"Error al eliminar: {e}")
