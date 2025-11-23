# auth/config.py
"""
Configuración del módulo de autenticación.
Lee variables desde os.environ (Streamlit secrets se inyectan en os.environ en Streamlit Cloud).
No guardes credenciales en el código.
"""

import os

# Modo de autenticación:
# - "db": autentica consultando una tabla en la base de datos (por ejemplo "Administrador")
# - "static": autentica comparando con credenciales guardadas en secrets como ADMIN_USER / ADMIN_PASS
AUTH_MODE = os.getenv("AUTH_MODE", "db")  # "db" o "static"

# Si AUTH_MODE == "db", estos son los parámetros que usará la consulta:
AUTH_TABLE = os.getenv("AUTH_TABLE", "Administrador")      # tabla donde están usuarios
AUTH_USER_COL = os.getenv("AUTH_USER_COL", "Correo")      # columna email/usuario
AUTH_PASS_COL = os.getenv("AUTH_PASS_COL", "Password")    # columna contraseña (o nombre real en tu BD)

# Tipo de hash de contraseña guardado en la base de datos:
# - "bcrypt" si usas bcrypt
# - "plain" si las contraseñas están en texto plano (no recomendado)
PASSWORD_HASH = os.getenv("PASSWORD_HASH", "plain")

# Si AUTH_MODE == "static", Streamlit secrets deben contener ADMIN_USER y ADMIN_PASS
ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASS = os.getenv("ADMIN_PASS")

# Secret key (opcional) para firmar sesiones o tokens si lo deseas
SECRET_KEY = os.getenv("SECRET_KEY", "please-change-me")
