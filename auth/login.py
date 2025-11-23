# auth/login.py
import streamlit as st
from db import get_session_local
from sqlalchemy import text
from .config import AUTH_MODE, AUTH_TABLE, AUTH_USER_COL, AUTH_PASS_COL, PASSWORD_HASH, ADMIN_USER, ADMIN_PASS
import traceback

try:
    import bcrypt
    _bcrypt_available = True
except Exception:
    _bcrypt_available = False

def authenticate_db(email: str, password: str):
    SessionLocal = get_session_local()
    session = SessionLocal()
    try:
        res = session.execute(text(f"SELECT * FROM `{AUTH_TABLE}` WHERE `{AUTH_USER_COL}` = :email LIMIT 1"), {"email": email})
        row = res.fetchone()
        if not row:
            return None
        user = dict(zip(res.keys(), row))
        stored = user.get(AUTH_PASS_COL)
        if stored is None:
            return None
        if PASSWORD_HASH == "bcrypt":
            if not _bcrypt_available:
                raise RuntimeError("bcrypt no instalado")
            if isinstance(stored, str):
                stored_b = stored.encode("utf-8")
            else:
                stored_b = stored
            if bcrypt.checkpw(password.encode("utf-8"), stored_b):
                return user
            return None
        else:
            if str(stored) == str(password):
                return user
            return None
    except Exception:
        st.error("Error autenticando con DB. Revisa logs.")
        st.write(traceback.format_exc())
        return None
    finally:
        session.close()

def authenticate_static(email: str, password: str):
    if ADMIN_USER is None or ADMIN_PASS is None:
        return None
    if str(email) == str(ADMIN_USER) and str(password) == str(ADMIN_PASS):
        return {"correo": ADMIN_USER, "rol": "admin"}
    return None

def _init_session_state():
    if "auth_user" not in st.session_state:
        st.session_state["auth_user"] = None
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

def logout():
    st.session_state["auth_user"] = None
    st.session_state["logged_in"] = False

def show_login_streamlit(title="Iniciar sesión", allow_logout=True):
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
                st.experimental_rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
    return None
