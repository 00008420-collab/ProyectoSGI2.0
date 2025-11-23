# crud.py
from db import SessionLocal
from sqlalchemy import text
import pandas as pd

def listar_tabla(tabla, limit=500):
    session = SessionLocal()
    try:
        res = session.execute(text(f"SELECT * FROM {tabla} LIMIT :lim"), {"lim": limit})
        cols = res.keys()
        rows = res.fetchall()
        return pd.DataFrame(rows, columns=cols)
    finally:
        session.close()
