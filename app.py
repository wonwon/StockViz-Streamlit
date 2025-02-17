import pandas as pd
import streamlit as st

from src.data_loader import fetch_stock_data
from src.db_manager import fetch_data, save_data_to_db

st.title("📊 TiDB Serverless & Streamlit")

# データ取得ボタン
if st.button("データ取得"):
    df = fetch_data()
    if df:
        st.dataframe(pd.DataFrame(df))
    else:
        st.warning("⚠️ データがありません。")

# データ保存ボタン
if st.button("データ保存"):
    with st.spinner("データ保存中..."):
        df = fetch_stock_data("4755")  # 株価データ取得
        if df is not None:
            save_data_to_db(df.to_records(index=False))
            st.success("✅ データを TiDB に保存しました！")
