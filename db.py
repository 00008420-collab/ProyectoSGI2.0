# db.py
import os
import urllib.parse
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

DB_PASS_ESC = urllib.parse.quote_plus(DB_PASS)

CONN = f"mysql+pymysql://{DB_USER}:{DB_PASS_ESC}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(CONN, echo=False, future=True)

metadata = MetaData()
metadata.reflect(bind=engine)
Base = automap_base(metadata=metadata)
Base.prepare()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_table_names():
    return list(metadata.tables.keys())

def get_table_columns(table_name):
    tbl = metadata.tables.get(table_name)
    if not tbl:
        return []
    return [c.name for c in tbl.columns]
