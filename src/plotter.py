import matplotlib.pyplot as plt


def plot_stock_chart(df, stock_code):
    """株価データをプロット"""
    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.plot(df.index, df["Close"], marker="o", linestyle="-", color="black", label="終値 (Close)")
    ax1.set_ylabel("株価 (円)")
    ax1.set_title(f"{stock_code} 株価推移")

    ax2 = ax1.twinx()
    ax2.bar(df.index, df["Volume"], color="blue", alpha=0.3, label="出来高 (Volume)")
    ax2.set_ylabel("出来高")

    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    return fig
