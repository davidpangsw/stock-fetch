import json
from pprint import pprint
import yfinance as yf

# DATE_END = "2022-01-01"     # end exclusive
INFO_KEYS = [
    'sector', 'industry',
    'country', 'state', 'exchange',
    'shortName', 'longName', 'symbol', 'market', 'marketCap',
    'longBusinessSummary', 'website',
]

ticker = yf.Ticker("MSFT")
json.dump(ticker.info, open("info/raw/msft.json", 'w'))
info = { key: ticker.info[key] for key in INFO_KEYS}
json.dump(info, open("info/msft.json", 'w'))
# symbols = ["META"]
# # symbols = ["AAPL", "MSFT", "SPY"]
# print(" ".join(symbols))
# history = yf.download(" ".join(symbols), end=DATE_END, group_by= 'ticker')
# print(history)