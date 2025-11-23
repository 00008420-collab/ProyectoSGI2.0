import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host='bewuh9yx8e9gctyl08lp-mysql.services.clever-cloud.com',
            user='uvfz1bhg53yj6hed',
            password='F2wwhaaKkEUbS4annYMP',
            database='bewuh9yx8e9gctyl08lp',
            port=3306
        )
        if conexion.is_connected():
            print("✅ Conexión establecida")
            return conexion
        else:
            print("❌ Conexión fallida (is_connected = False)")
            return None
    except mysql.connector.Error as e:
        print(f"❌ Error al conectar: {e}")
        return None
