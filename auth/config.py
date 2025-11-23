# auth/config.py
import os
AUTH_MODE = os.getenv("AUTH_MODE", "db")     # "db" o "static"
AUTH_TABLE = os.getenv("AUTH_TABLE", "Administrador")
AUTH_USER_COL = os.getenv("AUTH_USER_COL", "Correo")
AUTH_PASS_COL = os.getenv("AUTH_PASS_COL", "Password")
PASSWORD_HASH = os.getenv("PASSWORD_HASH", "plain")  # "plain" o "bcrypt"
ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASS = os.getenv("ADMIN_PASS")
SECRET_KEY = os.getenv("SECRET_KEY", "please-change-me")
