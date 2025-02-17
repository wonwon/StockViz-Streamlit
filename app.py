import streamlit as st

from src.data_loader import fetch_stock_data
from src.plotter import plot_stock_chart

st.title("📈 株価 & 信用取引データの可視化")

stock_code = st.text_input("📌 銘柄コードを入力（例: 7203）", "7203")

if st.button("データ取得"):
    df = fetch_stock_data(stock_code)
    # データを確認
    st.write("デバッグ: 取得データ", df.head())

    if df is None or df.empty:
        st.error("⚠️ データ取得に失敗しました。銘柄コードを確認してください。")
    else:
        fig = plot_stock_chart(df, stock_code)
        if fig is not None:
            st.pyplot(fig)
        else:
            st.error("⚠️ グラフが作成できませんでした。")
