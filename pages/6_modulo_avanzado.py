# pages/6_modulo_avanzado.py
import streamlit as st
from db import get_table_columns, get_table_names_safe
from crud_full import get_all, get_by_id, create, update
from db import get_session_local
from sqlalchemy import text

st.title("Módulo avanzado — Préstamos y Pagos")

def build_label_for_table(table_name, id_col="Id_miembro"):
    cols = get_table_columns(table_name) or []
    candidates = []
    if "Nombre" in cols and "Apellido" in cols:
        candidates.append(("concat","Nombre","Apellido"))
    elif "Apellido" in cols:
        candidates.append(("single","Apellido"))
    elif "Nombre" in cols:
        candidates.append(("single","Nombre"))
    session = get_session_local()()
    try:
        if any(c[0]=="concat" for c in candidates):
            sql = text(f"SELECT `{id_col}` as id, CONCAT(COALESCE(Nombre,''),' ',COALESCE(Apellido,'')) as label FROM `{table_name}`")
        elif candidates:
            col = candidates[0][1]
            sql = text(f"SELECT `{id_col}` as id, COALESCE(`{col}`,'') as label FROM `{table_name}`")
        else:
            sql = text(f"SELECT `{id_col}` as id, CAST(`{id_col}` AS CHAR) as label FROM `{table_name}`")
        res = session.execute(sql)
        rows = res.fetchall()
        return [(str(r[0]), r[1] if r[1] else str(r[0])) for r in rows]
    except Exception:
        return []
    finally:
        session.close()

st.header("Miembros")
miembro_opts = build_label_for_table("Miembro", id_col="Id_miembro")
if miembro_opts:
    sel = st.selectbox("Selecciona miembro", options=[f"{lab} ({_id})" for _id, lab in miembro_opts])
else:
    st.info("No se detectan miembros")

st.header("Crear préstamo")
cols_p = get_table_columns("Prestamo") or []
if cols_p:
    with st.form("crear_prestamo"):
        data = {}
        for c in cols_p:
            if c.lower() == "id_prestamo":
                continue
            if c.lower() in ("id_miembro",):
                data[c] = st.text_input(c, value=(miembro_opts[0][0] if miembro_opts else ""))
            elif "fecha" in c.lower():
                data[c] = st.date_input(c)
            else:
                data[c] = st.text_input(c)
        if st.form_submit_button("Crear préstamo"):
            serial = {}
            for k,v in data.items():
                if hasattr(v,"isoformat"):
                    serial[k] = v.isoformat()
                else:
                    serial[k] = v
            try:
                new = create("Prestamo", serial)
                st.success(f"Préstamo creado (Id: {new})")
            except Exception as e:
                st.error(e)
else:
    st.info("Tabla `Prestamo` no encontrada o sin columnas.")

st.header("Registrar pago")
prestamos = get_all("Prestamo", limit=500) if "Prestamo" in get_table_names_safe() else []
if prestamos:
    options = []
    for p in prestamos:
        pid = p.get("Id_prestamo") or p.get("id_prestamo")
        saldo = p.get("Saldo restante") or p.get("Saldo_restante") or p.get("Saldo") or ""
        options.append((str(pid), f"Préstamo {pid} | Saldo: {saldo}"))
    mapping = {lab: pid for pid, lab in options}
    sel_lab = st.selectbox("Selecciona préstamo", options=[lab for (_, lab) in options])
    sel_pid = mapping.get(sel_lab)
    if sel_pid:
        cols_pay = get_table_columns("Pago") or []
        with st.form("registrar_pago"):
            paydata = {}
            for c in cols_pay:
                if c.lower()=="id_pago":
                    continue
                if c.lower() in ("id_prestamo",):
                    paydata[c] = st.text_input(c, value=str(sel_pid))
                elif "fecha" in c.lower():
                    paydata[c] = st.date_input(c)
                else:
                    paydata[c] = st.text_input(c)
            if st.form_submit_button("Registrar pago"):
                serial = {}
                for k,v in paydata.items():
                    if hasattr(v,"isoformat"):
                        serial[k] = v.isoformat()
                    else:
                        serial[k] = v
                try:
                    new = create("Pago", serial)
                    st.success(f"Pago registrado (Id: {new})")
                except Exception as e:
                    st.error(e)
else:
    st.info("No hay préstamos cargados.")
