# db.py
import os
import urllib.parse

def _get_env(k, default=None):
    v = os.getenv(k)
    return v if v is not None else default

def make_conn_str():
    DB_USER = _get_env("DB_USER")
    DB_PASS = urllib.parse.quote_plus(_get_env("DB_PASS",""))
    DB_HOST = _get_env("DB_HOST")
    DB_PORT = _get_env("DB_PORT","3306")
    DB_NAME = _get_env("DB_NAME")
    if not all([DB_USER, DB_HOST, DB_NAME]):
        # no raise here: caller should handle empty env
        return None
    return f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

def get_engine():
    conn = make_conn_str()
    if not conn:
        raise RuntimeError("Faltan variables de entorno DB_* (revisa Secrets).")
    from sqlalchemy import create_engine
    return create_engine(conn, future=True)

def get_session_local():
    from sqlalchemy.orm import sessionmaker
    engine = get_engine()
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)

# utilitarios
def get_table_names_safe():
    """Devuelve lista de tablas o [] si no puede conectar."""
    try:
        SessionLocal = get_session_local()
        session = SessionLocal()
        try:
            res = session.execute("SHOW TABLES")
            return [r[0] for r in res.fetchall()]
        finally:
            session.close()
    except Exception:
        return []

def get_table_columns(table_name):
    """Devuelve columnas de una tabla (o [] si falla)."""
    try:
        SessionLocal = get_session_local()
        session = SessionLocal()
        try:
            res = session.execute(f"SELECT * FROM `{table_name}` LIMIT 1")
            return list(res.keys())
        finally:
            session.close()
    except Exception:
        return []
