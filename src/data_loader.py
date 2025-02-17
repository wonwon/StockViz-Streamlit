import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


def fetch_stock_data(stock_code):
    """株探（kabutan.jp）から株価データを取得"""
    url = f"https://kabutan.jp/stock/kabuka?code={stock_code}&ashi=shin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        time.sleep(2)  # 連続アクセスを避けるため2秒待機
        response = requests.get(url, headers=headers, timeout=10)
        print(f"HTTPステータスコード: {response.status_code}")

        if response.status_code != 200:
            return None

        print("デバッグ: 取得したHTMLの最初の1000文字")
        print(response.text[:1000])  # HTMLの一部を表示

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="stock_kabuka0")

        if table is None:
            print("⚠️ データのテーブルが見つかりませんでした。HTML構造が変わっている可能性があります。")
            return None

        print("デバッグ: 取得したテーブル", table)

        rows = table.find_all("tr")[1:]  # ヘッダーを除外
        data = []

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 6:
                continue

            date_text = cols[0].text.strip()
            close_price_text = cols[4].text.strip().replace(",", "")
            volume_text = cols[5].text.strip().replace(",", "")

            print(f"デバッグ: date_text={date_text}, close_price_text={close_price_text}, volume_text={volume_text}")

            if not date_text or date_text == "－":
                print("⚠️ 日付が不正なためスキップ")
                continue  # 無効な日付はスキップ

            try:
                close_price = float(close_price_text) if close_price_text.replace('.', '', 1).isdigit() else None
                volume = int(volume_text) if volume_text.isdigit() else None
            except ValueError:
                print(f"⚠️ データ変換エラー: close_price={close_price_text}, volume={volume_text}")
                close_price, volume = None, None  # エラーが発生したら None にする

            data.append([date_text, close_price, volume])


        df = pd.DataFrame(data, columns=["Date", "Close", "Volume"])

        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])  # NaT（変換できなかった日付）を削除
        df.set_index("Date", inplace=True)

        print("デバッグ: 取得したデータ")
        print(df.head())

        return df

    except requests.exceptions.RequestException as e:
        print(f"データ取得エラー: {e}")
        return None
