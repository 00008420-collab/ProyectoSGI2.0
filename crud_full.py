# crud_full.py
from db import SessionLocal, metadata
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

def get_all(table_name, limit=500):
    sql = text(f"SELECT * FROM `{table_name}` LIMIT :lim")
    session = SessionLocal()
    try:
        res = session.execute(sql, {"lim": limit})
        cols = res.keys()
        rows = res.fetchall()
        return [dict(zip(cols, r)) for r in rows]
    finally:
        session.close()

def get_by_id(table_name, id_col, id_val):
    sql = text(f"SELECT * FROM `{table_name}` WHERE `{id_col}` = :id_val LIMIT 1")
    session = SessionLocal()
    try:
        res = session.execute(sql, {"id_val": id_val})
        row = res.fetchone()
        if row is None:
            return None
        return dict(zip(res.keys(), row))
    finally:
        session.close()

def create(table_name, data: dict):
    if not data:
        raise ValueError("data vacío")
    cols = ", ".join(f"`{c}`" for c in data.keys())
    vals = ", ".join(f":{c}" for c in data.keys())
    sql = text(f"INSERT INTO `{table_name}` ({cols}) VALUES ({vals})")
    session = SessionLocal()
    try:
        res = session.execute(sql, data)
        session.commit()
        try:
            return res.lastrowid
        except Exception:
            return True
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()

def update(table_name, id_col, id_val, data: dict):
    if not data:
        raise ValueError("data vacío")
    set_clause = ", ".join(f"`{k}` = :{k}" for k in data.keys())
    params = data.copy()
    params["id_val"] = id_val
    sql = text(f"UPDATE `{table_name}` SET {set_clause} WHERE `{id_col}` = :id_val")
    session = SessionLocal()
    try:
        res = session.execute(sql, params)
        session.commit()
        return res.rowcount
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()

def delete(table_name, id_col, id_val):
    sql = text(f"DELETE FROM `{table_name}` WHERE `{id_col}` = :id_val")
    session = SessionLocal()
    try:
        res = session.execute(sql, {"id_val": id_val})
        session.commit()
        return res.rowcount
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_columns(table_name):
    tbl = metadata.tables.get(table_name)
    if not tbl:
        return []
    return [c.name for c in tbl.columns]
