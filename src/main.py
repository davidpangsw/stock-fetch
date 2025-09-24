from yahoo import Yahoo
from database import STOCK_REPO
from symbols import getSymbols

NUMBER_OF_SYMBOLS = 20
DATE_START = "2024-09-23" 
DATE_END = "2025-09-23"     # end exclusive

# symbols = getSymbols(NUMBER_OF_SYMBOLS)
symbols = ['AAPL', 'HON']
yahoo = Yahoo(repo=STOCK_REPO, dump_dir=None)
yahoo.reset(symbols, price_start=DATE_START, price_end=DATE_END)

print("main.py done")