import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


def fetch_stock_data(stock_code):
    """株探（kabutan.jp）の指定テーブル（//*[@id="stock_kabuka_table"]/table[2]）から株価データを取得"""
    url = f"https://kabutan.jp/stock/kabuka?code={stock_code}&ashi=shin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    time.sleep(5)  # 5秒待機

    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=30)
    except requests.exceptions.RequestException as e:
        print(f"⚠️ リクエストエラー: {e}")
        return None

    if response.status_code != 200:
        print(f"⚠️ HTTPエラー: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # 指定のテーブルを取得
    tables = soup.select("#stock_kabuka_table table")
    if len(tables) < 2:
        print("⚠️ エラー: 指定のテーブルが見つかりません")
        return None

    table = tables[1]  # 2番目のテーブルを取得
    rows = table.find_all("tr")[1:]  # ヘッダー行を除外

    data = []
    for row in rows:
        date_col = row.find("th")  # `th` 要素を取得
        if date_col:
            date_time_tag = date_col.find("time")  # `time` タグを取得
            if date_time_tag:
                date_text = date_time_tag["datetime"].strip()
            else:
                print(f"⚠️ timeタグが見つかりません: {date_col}")
                continue
        else:
            print(f"⚠️ thタグが見つかりません: {row}")
            continue

        cols = row.find_all("td")

        # デバッグ: `cols` の要素数を表示
        print(f"デバッグ: {date_text} のデータ列数 → {len(cols)}")

        if len(cols) < 7:
            print("⚠️ データが不足しています。スキップします。")
            continue  

        try:
            close_price_text = cols[0].text.strip().replace(",", "")
            trade_price_text = cols[2].text.strip().replace(",", "")
            volume_text = cols[3].text.strip().replace(",", "").replace("万", "")
            sell_balance_text = cols[4].text.strip().replace(",", "").replace("－", "0")
            buy_balance_text = cols[5].text.strip().replace(",", "").replace("－", "0")
            credit_ratio_text = cols[6].text.strip().replace("－", "0")

            # 型変換
            date_text = pd.to_datetime(date_text, errors="coerce")
            close_price = float(close_price_text)
            trade_price = float(trade_price_text)
            volume = float(volume_text) * 10000 if "万" in cols[3].text else int(volume_text)
            sell_balance = int(sell_balance_text) if sell_balance_text.isdigit() else 0
            buy_balance = int(buy_balance_text) if buy_balance_text.isdigit() else 0
            credit_ratio = float(credit_ratio_text) if credit_ratio_text.replace(".", "").isdigit() else 0

            # デバッグログ
            print(f"✅ データ取得成功: date_text={date_text}, close_price={close_price}, trade_price={trade_price}, volume={volume}, "
                  f"sell_balance={sell_balance}, buy_balance={buy_balance}, credit_ratio={credit_ratio}")

            data.append([date_text, close_price, trade_price, volume, sell_balance, buy_balance, credit_ratio])

        except ValueError as e:
            print(f"⚠️ データ取得エラー: {e} | date={date_text}, close_price={close_price_text}, trade_price={trade_price_text}, volume={volume_text}, "
                  f"sell_balance={sell_balance_text}, buy_balance={buy_balance_text}, credit_ratio={credit_ratio_text}")
            continue

    # DataFrameを作成
    df = pd.DataFrame(data, columns=["Date", "Close", "Trade Price", "Volume", "Sell Balance", "Buy Balance", "Credit Ratio"])
    df.dropna(subset=["Date"], inplace=True)
    df.set_index("Date", inplace=True)

    return df