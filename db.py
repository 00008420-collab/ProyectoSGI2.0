# db_safe.py (rename to db.py en tu repo)
import os
import urllib.parse

# IMPORTS perezosos para que la app no falle si falta un paquete
def make_engine():
    try:
        from sqlalchemy import create_engine
    except Exception:
        raise
    DB_USER = os.getenv("DB_USER")
    DB_PASS = urllib.parse.quote_plus(os.getenv("DB_PASS",""))
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT","3306")
    DB_NAME = os.getenv("DB_NAME")
    conn = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    return create_engine(conn, future=True)

# crear metadata/metadata.reflect solo cuando se necesite
def get_session():
    from sqlalchemy.orm import sessionmaker
    engine = make_engine()
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return SessionLocal()

# utilitarios simples que usan sesiones bajo demanda
def show_tables():
    session = get_session()()
    try:
        res = session.execute("SHOW TABLES")
        return [r[0] for r in res.fetchall()]
    finally:
        session.close()
