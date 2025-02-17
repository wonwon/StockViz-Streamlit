import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def plot_stock_chart(df, stock_code):
    """株価と信用取引データを可視化する"""
    
    # デバッグ用の出力
    print(f"デバッグ: dfの型 → {type(df)}")
    print(f"デバッグ: df.indexの型 → {type(df.index)}")

    # `df` が `None` でないことを確認
    if df is None:
        print("⚠️ `df` が None です。データ取得に失敗している可能性があります。")
        return None

    df.index = pd.to_datetime(df.index)
    
    # グラフの描画
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # 終値の折れ線グラフ（黒線）
    ax1.plot(df.index, df["Close"], marker="o", linestyle="-", color="black", label="終値 (Close)")
    ax1.set_ylabel("株価 (円)", color="black")
    ax1.set_title(f"{stock_code} 株価と信用取引データ")
    
    # 第2軸（信用取引データ）
    ax2 = ax1.twinx()
    ax2.bar(df.index, df["Buy Balance"], color="blue", alpha=0.3, label="買い残")
    ax2.bar(df.index, -df["Sell Balance"], color="red", alpha=0.3, label="売り残")  # 売り残は負の方向に描画
    ax2.plot(df.index, df["Credit Ratio"] * 100000, color="purple", linestyle="dashed", label="信用倍率 (×10万)")
    ax2.set_ylabel("信用取引 (株) / 信用倍率", color="black")
    
    # 凡例の追加
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
    
    # X軸の回転
    plt.xticks(rotation=45)
    
    return fig

# Streamlit アプリのUI
st.title("📈 株価データ可視化アプリ")

stock_code = st.text_input("銘柄コードを入力してください（例: 4755）", "4755")

if st.button("データ取得"):
    with st.spinner("データ取得中..."):
        df = fetch_stock_data(stock_code)
        if df is not None:
            st.success("✅ データ取得成功！")
            st.dataframe(df)

            # 株価の推移をプロット
            st.line_chart(df["Close"])

            # 出来高の推移をプロット
            st.bar_chart(df["Volume"])
