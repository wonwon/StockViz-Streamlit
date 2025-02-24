import pandas as pd
import streamlit as st

from src.db_connector import fetch_stock_data

st.title("📈 株価データ可視化アプリ")

# データ取得
data = fetch_stock_data()

# DataFrame に変換して表示
df = pd.DataFrame(data, columns=["Date", "Close Price", "Trade Price", "Volume", "Sell Balance", "Buy Balance", "Credit Ratio"])
st.dataframe(df)

# グラフ表示
st.line_chart(df.set_index("Date")["Close Price"])
