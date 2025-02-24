import mysql.connector
import streamlit as st

# Streamlit Secrets から DB 接続情報を取得
DB_CONFIG = {
    "host": st.secrets["DB_HOST"],
    "port": st.secrets["DB_PORT"],
    "user": st.secrets["DB_USER"],
    "password": st.secrets["DB_PASSWORD"],
    "database": st.secrets["DB_NAME"],
    "ssl_ca": st.secrets["DB_SSL_CA"]
}

def get_connection():
    """TiDB への接続を作成"""
    return mysql.connector.connect(**DB_CONFIG)

def fetch_stock_data():
    """ストックデータを取得"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stock_data;")
    data = cursor.fetchall()
    conn.close()
    return data
