# db.py
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

DB_USER = os.getenv("DB_USER", "uvfz1bhg53yj6hed")
DB_PASS = os.getenv("DB_PASS", "F2wwhaaKkEUbS4annYMP")
DB_HOST = os.getenv("DB_HOST", "bewuh9yx8e9gctyl08lp-mysql.services.clever-cloud.com")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "bewuh9yx8e9gctyl08lp")

CONN = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(CONN, echo=False, future=True)

# Reflect existing DB
metadata = MetaData()
metadata.reflect(bind=engine)
Base = automap_base(metadata=metadata)
Base.prepare()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_table_names():
    return list(metadata.tables.keys())
