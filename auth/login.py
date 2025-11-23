# auth/login.py
"""
Lógica de autenticación. Funciona en dos modos:
 - DB: consulta la tabla configurada (AUTH_TABLE) para validar usuario.
 - STATIC: compara contra ADMIN_USER / ADMIN_PASS en secrets.

Incluye helper `show_login_streamlit()` para usar desde Streamlit:
  user = show_login_streamlit()
  if user:
      # usuario autenticado -> mostrar la app
"""
import streamlit as st
from db import SessionLocal
from sqlalchemy import text
from .config import (
    AUTH_MODE,
    AUTH_TABLE,
    AUTH_USER_COL,
    AUTH_PASS_COL,
    PASSWORD_HASH,
    ADMIN_USER,
    ADMIN_PASS,
)
import traceback

# intentamos importar bcrypt; si no está, fallback a comparación en texto plano
try:
    import bcrypt  # pip install bcrypt
    _bcrypt_available = True
except Exception:
    _bcrypt_available = False


def authenticate_db(email: str, password: str):
    """Consulta la tabla AUTH_TABLE por email (AUTH_USER_COL) y compara la contraseña.
    Devuelve el diccionario del usuario (fila) si ok, o None.
    """
    session = SessionLocal()
    try:
        sql = text(f"SELECT * FROM `{AUTH_TABLE}` WHERE `{AUTH_USER_COL}` = :email LIMIT 1")
        res = session.execute(sql, {"email": email})
        row = res.fetchone()
        if not row:
            return None
        keys = res.keys()
        user = dict(zip(keys, row))

        stored = user.get(AUTH_PASS_COL)
        if stored is None:
            # no hay columna de password con ese nombre
            return None

        # comparar según tipo de hash
        if PASSWORD_HASH == "bcrypt":
            if not _bcrypt_available:
                # no podemos comprobar bcrypt si no está instalado
                raise RuntimeError("bcrypt no está instalado en el entorno. Agrega 'bcrypt' en requirements.txt")
            # stored should be bytes; ensure correct type
            if isinstance(stored, str):
                stored_b = stored.encode("utf-8")
            else:
                stored_b = stored
            ok = bcrypt.checkpw(password.encode("utf-8"), stored_b)
            return user if ok else None
        else:
            # plain text comparison (no recomendado)
            if str(stored) == str(password):
                return user
            return None
    except Exception:
        st.error("Error autenticando con DB (ver consola).")
        st.write(traceback.format_exc())
        return None
    finally:
        session.close()


def authenticate_static(email: str, password: str):
    """Comprueba contra ADMIN_USER / ADMIN_PASS (útil para pruebas)."""
    if ADMIN_USER is None or ADMIN_PASS is None:
        return None
    if str(email) == str(ADMIN_USER) and str(password) == str(ADMIN_PASS):
        return {"correo": ADMIN_USER, "rol": "admin"}
    return None


# ---------- Streamlit helper ----------
def _init_session_state():
    if "auth_user" not in st.session_state:
        st.session_state["auth_user"] = None
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False


def logout():
    st.session_state["auth_user"] = None
    st.session_state["logged_in"] = False


def show_login_streamlit(title="Iniciar sesión", allow_logout=True):
    """
    Muestra el formulario de login en Streamlit.
    Retorna el objeto usuario (dict) si autenticado, o None.
    Usa st.session_state para mantener la sesión dentro de Streamlit.
    """
    _init_session_state()

    if st.session_state.get("logged_in") and st.session_state.get("auth_user"):
        if allow_logout:
            with st.expander("Sesión"):
                st.write("Conectado como:", st.session_state["auth_user"])
                if st.button("Cerrar sesión"):
                    logout()
                    st.experimental_rerun()
        return st.session_state["auth_user"]

    st.header(title)
    with st.form("login_form"):
        email = st.text_input("Correo / usuario")
        pwd = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Entrar")
        if submitted:
            if AUTH_MODE == "db":
                user = authenticate_db(email, pwd)
            else:
                user = authenticate_static(email, pwd)

            if user:
                st.success("Autenticación correcta")
                st.session_state["auth_user"] = user
                st.session_state["logged_in"] = True
                # rerun para que la app muestre la vista autenticada
                st.experimental_rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
    return None
