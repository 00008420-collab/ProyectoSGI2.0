# auth/__init__.py
"""
API pública del paquete auth.
Importa show_login_streamlit para usar en tus páginas Streamlit.
"""
from .login import (
    authenticate_db,
    authenticate_static,
    show_login_streamlit,
    logout,
)

__all__ = [
    "authenticate_db",
    "authenticate_static",
    "show_login_streamlit",
    "logout",
]
