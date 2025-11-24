# db.py
"""
db.py - utilitarios seguros para conectarse a MySQL usando SQLAlchemy + PyMySQL.
No realiza conexiones en import time: crea engine/session SOLO cuando se solicita.
Requiere que las siguientes variables de entorno estén definidas (Streamlit Secrets):
 - DB_HOST
 - DB_PORT
 - DB_USER
 - DB_PASS
 - DB_NAME

Funciones principales:
 - get_engine()
 - get_session_local()
 - get_table_names_safe()
 - get_table_columns(table_name)
 - test_connection()
"""

import os
import urllib.parse
import logging

_logger = logging.getLogger(__name__)


def _env(k):
    return os.getenv(k)


def _make_conn_str():
    user = _env("DB_USER")
    pwd = _env("DB_PASS") or ""
    host = _env("DB_HOST")
    port = _env("DB_PORT") or "3306"
    name = _env("DB_NAME")
    if not (user and host and name):
        return None
    pwd_esc = urllib.parse.quote_plus(pwd)
    return f"mysql+pymysql://{user}:{pwd_esc}@{host}:{port}/{name}?charset=utf8mb4"


def get_engine():
    """
    Crea y devuelve un SQLAlchemy engine. Lanza RuntimeError si faltan variables DB_*.
    """
    conn = _make_conn_str()
    if not conn:
        raise RuntimeError(
            "Faltan variables de entorno DB_USER/DB_HOST/DB_NAME (revisa Secrets)."
        )
    # import local para evitar fallos en import-time si SQLAlchemy/pymysql no están instalados
    from sqlalchemy import create_engine

    engine = create_engine(conn, future=True)
    return engine


def get_session_local():
    """
    Devuelve sessionmaker enlazado al engine. No inicia la conexión hasta que se use la sesión.
    """
    from sqlalchemy.orm import sessionmaker

    engine = get_engine()
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_table_names_safe():
    """
    Devuelve lista de tablas en la BD. En caso de error, devuelve [] y registra la excepción.
    """
    try:
        SessionLocal = get_session_local()
        session = SessionLocal()
        try:
            res = session.execute("SHOW TABLES")
            return [r[0] for r in res.fetchall()]
        finally:
            session.close()
    except Exception as e:
        _logger.exception("get_table_names_safe: error conectando a la BD")
        return []


def get_table_columns(table_name):
    """
    Devuelve lista de columnas de una tabla o [] si no existe o hay error.
    """
    if not table_name:
        return []
    try:
        SessionLocal = get_session_local()
        session = SessionLocal()
        try:
            res = session.execute(f"SELECT * FROM `{table_name}` LIMIT 1")
            return list(res.keys())
        finally:
            session.close()
    except Exception as e:
        _logger.exception("get_table_columns: error leyendo columnas de %s", table_name)
        return []


def test_connection():
    """
    Intenta una consulta simple para validar la conexión (devuelve True/False y mensaje).
    """
    try:
        SessionLocal = get_session_local()
        session = SessionLocal()
        try:
            session.execute("SELECT 1")
            return True, "Conexión OK"
        finally:
            session.close()
    except Exception as e:
        _logger.exception("test_connection: fallo")
        return False, str(e)
