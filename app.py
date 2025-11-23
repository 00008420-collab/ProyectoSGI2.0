# app.py (DEBUG)
import streamlit as st
st.set_page_config(page_title="Debug GAPC", layout="centered")
st.title("Debug — Streamlit app running ✅")

import os
st.subheader("Check environment")
for k in ["DB_HOST","DB_NAME","DB_USER","DB_PASS","DB_PORT","AUTH_MODE"]:
    st.write(k, "=", "✓" if os.getenv(k) else "— no definida —")

st.subheader("Check Python modules")
errors = []
try:
    import sqlalchemy
except Exception as e:
    errors.append(f"sqlalchemy: {e}")
try:
    import pymysql
except Exception as e:
    errors.append(f"pymysql: {e}")
try:
    import pandas
except Exception as e:
    errors.append(f"pandas: {e}")

if not errors:
    st.success("Módulos esenciales importados OK")
else:
    st.error("Error importando módulos (ver abajo)")
    for e in errors:
        st.write(e)
