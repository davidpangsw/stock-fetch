from yahoo import Yahoo
from database import STOCK_REPO
from symbols import get_symbols, scrape_symbols
from config import NUMBER_OF_SYMBOLS, DATE_START, DATE_END

symbols = scrape_symbols()[:NUMBER_OF_SYMBOLS]
# symbols = get_symbols(NUMBER_OF_SYMBOLS)
# symbols = ['AAPL', 'HON']
yahoo = Yahoo(repo=STOCK_REPO, dump_dir=None)
yahoo.reset(symbols, price_start=DATE_START, price_end=DATE_END)

print("main.py done")