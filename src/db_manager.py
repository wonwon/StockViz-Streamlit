import mysql.connector
import streamlit as st

# Streamlit Secrets からDB接続情報を取得
DB_CONFIG = {
    "host": st.secrets["DB_HOST"],
    "port": int(st.secrets["DB_PORT"]),
    "user": st.secrets["DB_USER"],
    "password": st.secrets["DB_PASSWORD"],
    "database": st.secrets["DB_DATABASE"],
    "ssl_ca": st.secrets["DB_SSL_CA"],  # SSL証明書の設定
}

# データベースに接続
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# データを取得
def fetch_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM stock_data ORDER BY date DESC LIMIT 10")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# データを保存
def save_data_to_db(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_data (
            date DATE PRIMARY KEY,
            close_price FLOAT,
            trade_price FLOAT,
            volume INT,
            sell_balance INT,
            buy_balance INT,
            credit_ratio FLOAT
        )
    """)
    for row in data:
        cursor.execute("""
            INSERT INTO stock_data (date, close_price, trade_price, volume, sell_balance, buy_balance, credit_ratio)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                close_price=VALUES(close_price),
                trade_price=VALUES(trade_price),
                volume=VALUES(volume),
                sell_balance=VALUES(sell_balance),
                buy_balance=VALUES(buy_balance),
                credit_ratio=VALUES(credit_ratio)
        """, row)
    conn.commit()
    cursor.close()
    conn.close()
