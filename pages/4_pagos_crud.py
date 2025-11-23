import streamlit as st
from crud_full import get_all, get_by_id, create, update, delete, get_columns

TABLE = "Pago"
ID_COL = "Id_pago"

st.title("Pagos — CRUD")
cols = get_columns(TABLE)
st.write("Columnas:", cols)

with st.expander("Listar pagos"):
    st.dataframe(get_all(TABLE))

st.subheader("Registrar pago")
with st.form("create_pago"):
    data = {}
    for c in cols:
        if c == ID_COL:
            continue
        data[c] = st.text_input(c, "")
    s = st.form_submit_button("Registrar")
    if s:
        try:
            new = create(TABLE, data)
            st.success(f"Pago registrado (Id: {new})")
        except Exception as e:
            st.error(e)

st.subheader("Buscar / Editar / Eliminar pago")
pid = st.text_input("Id pago", "")
if st.button("Cargar pago"):
    rec = get_by_id(TABLE, ID_COL, pid)
    if not rec:
        st.info("No encontrado")
    else:
        st.json(rec)
        with st.form("update_pago"):
            upd = {}
            for c in cols:
                if c == ID_COL:
                    st.text_input(c, value=str(rec.get(c)), disabled=True)
                else:
                    upd[c] = st.text_input(c, value=str(rec.get(c) or ""))
            if st.form_submit_button("Actualizar"):
                try:
                    update(TABLE, ID_COL, pid, upd)
                    st.success("Actualizado")
                except Exception as e:
                    st.error(e)
        if st.button("Eliminar pago"):
            try:
                delete(TABLE, ID_COL, pid)
                st.success("Eliminado")
            except Exception as e:
                st.error(e)
