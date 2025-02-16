import pandas as pd
import requests
from bs4 import BeautifulSoup


def fetch_stock_data(stock_code):
    """株探（kabutan.jp）から株価データを取得"""
    url = f"https://kabutan.jp/stock/kabuka?code={stock_code}&ashi=shin"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="stock_kabuka0")
    rows = table.find_all("tr")[1:]

    data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 6:
            continue
        date = cols[0].text.strip()
        close_price = float(cols[4].text.replace(",", ""))
        volume = int(cols[5].text.replace(",", ""))
        data.append([date, close_price, volume])

    df = pd.DataFrame(data, columns=["Date", "Close", "Volume"])
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)
    
    return df
