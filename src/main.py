from yahoo import Yahoo
from database import STOCK_REPO
from symbols import get_symbols, scrape_symbols
from config import NUMBER_OF_SYMBOLS, DATE_START, DATE_END, DIR_DATA

# import yfinance as yf
# ticker = yf.Ticker("VG")
# doc = ticker.info
# data =  {
#                     "name": doc.get('longName', doc.get('shortName', None)),
#                     "shortName": doc.get('shortName', None),
#                     "longName": doc.get('longName', None),
#                     "symbol": doc['symbol'],
#                     # "lastUpdated": self.timestamp_to_string(doc['lastUpdated']),
#                 }
# print(data)
# import sys
# sys.exit()

symbols = scrape_symbols()[:NUMBER_OF_SYMBOLS]
# symbols = get_symbols(NUMBER_OF_SYMBOLS)
# symbols = ['AAPL', 'HON']
yahoo = Yahoo(repo=STOCK_REPO, dump_dir=DIR_DATA)
yahoo.reset(symbols, price_start=DATE_START, price_end=DATE_END)

print("main.py done")