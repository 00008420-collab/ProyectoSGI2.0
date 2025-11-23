# pages/6_modulo_avanzado.py
"""
Módulo avanzado — UI más amigable con selects legibles.
Funciones:
- Crear préstamo (elige miembro por etiqueta legible)
- Registrar pago (elige préstamo, muestra saldo)
- CRUD rápido de miembros (crear / listar)
Requiere: crud_full.py y db.py del proyecto.
"""
import streamlit as st
from db import get_table_columns
from crud_full import (
    get_all,
    get_by_id,
    create,
    update,
    delete,
)
from sqlalchemy import text
from db import SessionLocal

st.set_page_config(page_title="Módulo avanzado — GAPC", layout="wide")
st.title("Módulo avanzado — Préstamos y Pagos")

# ---------- Helpers ----------
def build_label_for_table(table_name, id_col="Id_miembro"):
    """
    Construye una etiqueta legible para cada registro de una tabla.
    Para Miembro:
      - Usa 'Nombre' + 'Apellido' si existen
      - Si no, usa 'Apellido'
      - Si no existe, usa el id
    Para otras tablas intenta detectar columnas 'Nombre' o 'Descripcion' u 'Apellido'
    Devuelve lista de tuplas (id, label).
    """
    cols = get_table_columns_safe(table_name)
    # Candidate columns for label, ordered by preference
    candidates = []
    if "Nombre" in cols and "Apellido" in cols:
        candidates.append(("concat", "Nombre", "Apellido"))
    if "Apellido" in cols and "Nombre" not in cols:
        candidates.append(("single", "Apellido"))
    if "Nombre" in cols and "Apellido" not in cols:
        candidates.append(("single", "Nombre"))
    if "DUI" in cols:
        candidates.append(("single", "DUI"))
    if "Nombre" in cols:
        candidates.append(("single", "Nombre"))
    if "Descripcion" in cols:
        candidates.append(("single", "Descripcion"))
    # Fallback: use id_col
    # Build SQL dynamically depending on available columns
    session = SessionLocal()
    try:
        if any(c[0] == "concat" for c in candidates):
            # prefer concat Nombre + Apellido
            sql = text(f"SELECT `{id_col}` as id, CONCAT(COALESCE(Nombre,''), ' ', COALESCE(Apellido,'')) as label FROM `{table_name}`")
        elif candidates:
            # use first candidate single column
            c = candidates[0]
            colname = c[1]
            sql = text(f"SELECT `{id_col}` as id, COALESCE(`{colname}`,'') as label FROM `{table_name}`")
        else:
            sql = text(f"SELECT `{id_col}` as id, CAST(`{id_col}` AS CHAR) as label FROM `{table_name}`")
        res = session.execute(sql)
        rows = res.fetchall()
        return [(str(r[0]), r[1] if r[1] is not None else str(r[0])) for r in rows]
    except Exception:
        # fallback: empty list
        return []
    finally:
        session.close()

def get_table_columns_safe(table_name):
    try:
        return get_table_columns(table_name)
    except Exception:
        # If get_table_columns isn't available in this environment, return empty
        try:
            from db import get_table_names
            if table_name in get_table_names():
                # minimal: try to introspect via a session
                sess = SessionLocal()
                try:
                    res = sess.execute(text(f"SELECT * FROM `{table_name}` LIMIT 1"))
                    return list(res.keys())
                finally:
                    sess.close()
        except Exception:
            return []
    return []

# ---------- Sección: Miembros (CRUD rápido con select) ----------
st.header("Miembros — Crear y seleccionar")

with st.expander("Crear nuevo miembro"):
    cols = get_table_columns_safe("Miembro")
    if not cols:
        st.warning("No se detecta la tabla `Miembro` o no tiene columnas. Verifica que la BD y nombres estén correctos.")
    else:
        # mostramos inputs para las columnas (excepto PK si es autoincrementable)
        inputs = {}
        pk = None
        for c in cols:
            if c.lower().startswith("id_") or c.lower().endswith("_id") or c.lower().startswith("id"):
                # posible PK, lo mostramos pero no obligatorio
                if "miembro" in c.lower():
                    pk = c
                continue
        # build form
        with st.form("crear_miembro"):
            for c in cols:
                if c == pk:
                    continue
                # usa tipos simples: text, number heurístico
                if "fecha" in c.lower():
                    inputs[c] = st.date_input(label=c)
                else:
                    inputs[c] = st.text_input(label=c)
            if st.form_submit_button("Crear miembro"):
                # serializar date -> str si aplica
                to_send = {}
                for k, v in inputs.items():
                    if hasattr(v, "isoformat"):
                        to_send[k] = v.isoformat()
                    else:
                        to_send[k] = v
                try:
                    new = create("Miembro", to_send)
                    st.success(f"Miembro creado (id: {new})")
                except Exception as e:
                    st.error(f"Error creando miembro: {e}")

st.markdown("---")
# Select para elegir miembro (legible)
miembro_options = build_label_for_table("Miembro", id_col="Id_miembro")
miembro_map = {label: id_ for id_, label in miembro_options}
sel_miembro_label = st.selectbox("Selecciona un miembro", options=["-- Nuevo / seleccionar --"] + [lab for (_, lab) in miembro_options])
selected_miembro_id = None
if sel_miembro_label and sel_miembro_label != "-- Nuevo / seleccionar --":
    # find id for that label
    # invert map
    inv = {v: k for k, v in miembro_map.items()}
    # miembro_map is id->label stored earlier; build inverted properly
    found_id = None
    for _id, label in miembro_options:
        if label == sel_miembro_label:
            found_id = _id
            break
    if found_id:
        selected_miembro_id = found_id
        st.info(f"Miembro seleccionado: id = {selected_miembro_id}")

# ---------- Sección: Crear Préstamo (con select de miembro) ----------
st.header("Crear préstamo")
cols_p = get_table_columns_safe("Prestamo")
if not cols_p:
    st.warning("No se detecta la tabla `Prestamo` o no tiene columnas.")
else:
    with st.form("crear_prestamo"):
        # mostramos un select para elegir miembro (por id)
        miembro_choice = st.selectbox("Miembro (para préstamo)", options=[("","-- Selecciona --")] + [(mid, lab) for mid, lab in miembro_options], format_func=lambda x: x[1] if isinstance(x, tuple) else x)
        # miembro_choice is tuple (id,label) or "" — normalize
        if miembro_choice == "" or miembro_choice is None:
            mi_id = None
        else:
            mi_id = miembro_choice[0]
        inputs_p = {}
        for c in cols_p:
            if c.lower() == "id_prestamo":
                continue
            # if column references Id_miembro, prefill with selected
            if c.lower() in ("id_miembro", "id_miembro"):
                inputs_p[c] = st.text_input(c, value=mi_id or "")
            elif "fecha" in c.lower():
                inputs_p[c] = st.date_input(c)
            else:
                inputs_p[c] = st.text_input(c)
        if st.form_submit_button("Crear préstamo"):
            data = {}
            for k, v in inputs_p.items():
                if hasattr(v, "isoformat"):
                    data[k] = v.isoformat()
                else:
                    data[k] = v
            try:
                new_id = create("Prestamo", data)
                st.success(f"Préstamo creado (id: {new_id})")
            except Exception as e:
                st.error(f"Error creando préstamo: {e}")

st.markdown("---")
# ---------- Sección: Registrar Pago (elige préstamo) ----------
st.header("Registrar pago")
# Build options for Prestamo: label with Id + miembro label + saldo si existe
def build_prestamo_options():
    # try to get columns Id_prestamo, Id_miembro, Saldo restante (maybe 'Saldo restante' or 'Saldo restante' with spaces)
    session = SessionLocal()
    try:
        # attempt common column names
        # collect candidate label parts
        sql = text("SELECT * FROM `Prestamo` LIMIT 500")
        res = session.execute(sql)
        cols = res.keys()
        rows = res.fetchall()
        options = []
        for r in rows:
            rowd = dict(zip(cols, r))
            pid = rowd.get("Id_prestamo") or rowd.get("id_prestamo") or rowd.get("Id_Prestamo") or ""
            mid = rowd.get("Id_miembro") or rowd.get("id_miembro") or ""
            saldo = rowd.get("Saldo restante") or rowd.get("Saldo_restante") or rowd.get("Saldo") or ""
            label_parts = [f"Préstamo {pid}"]
            if mid:
                # try to get member label
                try:
                    # get member label
                    mlabel = None
                    mres = session.execute(text("SELECT Id_miembro, COALESCE(Nombre, '') as Nombre, COALESCE(Apellido, '') as Apellido FROM `Miembro` WHERE Id_miembro = :mid LIMIT 1"), {"mid": mid})
                    mr = mres.fetchone()
                    if mr:
                        mlabel = (mr[1] + " " + mr[2]).strip()
                    if mlabel:
                        label_parts.append(f"Miembro: {mlabel}")
                except Exception:
                    pass
            if saldo is not None and saldo != "":
                label_parts.append(f"Saldo: {saldo}")
            options.append((str(pid), " | ".join(label_parts)))
        return options
    except Exception:
        return []
    finally:
        session.close()

prestamo_options = build_prestamo_options()
if not prestamo_options:
    st.info("No se detectaron préstamos (tabla `Prestamo` vacía o no existe).")
else:
    # build select
    mapping = {lab: pid for pid, lab in prestamo_options}
    sel_label = st.selectbox("Selecciona préstamo", options=[lab for (_, lab) in prestamo_options])
    sel_pid = mapping.get(sel_label)
    st.write("Préstamo seleccionado:", sel_pid)

    with st.form("registrar_pago"):
        cols_pago = get_table_columns_safe("Pago")
        inputs_pay = {}
        for c in cols_pago:
            if c.lower() == "id_pago":
                continue
            # if column is Id_prestamo, set it
            if c.lower() in ("id_prestamo",):
                inputs_pay[c] = st.text_input(c, value=sel_pid or "")
            elif "fecha" in c.lower():
                inputs_pay[c] = st.date_input(c)
            else:
                inputs_pay[c] = st.text_input(c)
        if st.form_submit_button("Registrar pago"):
            pdata = {}
            for k, v in inputs_pay.items():
                if hasattr(v, "isoformat"):
                    pdata[k] = v.isoformat()
                else:
                    pdata[k] = v
            try:
                new = create("Pago", pdata)
                st.success(f"Pago registrado (id: {new})")
            except Exception as e:
                st.error(f"Error registrando pago: {e}")

# ---------- Enlace al PDF del proyecto ----------
st.markdown("---")
st.markdown("Documentación del proyecto:")
# ruta local al PDF que subiste (se incluye en el repo / zip)
pdf_path = "/mnt/data/Proyecto final rev.pdf"
st.markdown(f"- [Proyecto final (PDF)]({pdf_path})")
