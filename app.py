import streamlit as st

from src.data_loader import fetch_stock_data
from src.plotter import plot_stock_chart

# Streamlit UI
st.title("📈 株価 & 信用取引データの可視化")

stock_code = st.text_input("📌 銘柄コードを入力（例: 7203）", "7203")

if st.button("データ取得"):
    df = fetch_stock_data(stock_code)
    if df is None:
        st.error("⚠️ データ取得に失敗しました。銘柄コードを確認してください。")
    else:
        fig = plot_stock_chart(df, stock_code)
        st.pyplot(fig)

