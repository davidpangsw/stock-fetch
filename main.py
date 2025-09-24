from yahoo import Yahoo
from database import STOCK_REPO

DIR_DATA = Path('./data')
INFO_KEYS = [
    'sector', 'industry',
    'country', 'exchange',
    'shortName', 'longName', 'symbol', 'market', 'marketCap',
    'longBusinessSummary', 'website',
]
NUMBER_OF_SYMBOLS = 20
DATE_END = "2025-09-23"     # end exclusive

def getSymbols(n=None):
    with open(f'{DIR_DATA}/symbols/symbols.txt') as file:
        lines = [line.rstrip() for line in file]
    with open(f'{DIR_DATA}/symbols/blacklist.txt') as file:
        blacklist = [line.rstrip() for line in file]
    
    lines = filter(lambda i: i not in blacklist, lines)
    lines = lines if n is None else list(lines)[0:n]
    return lines

# symbols = getSymbols(NUMBER_OF_SYMBOLS)
symbols = ['AAPL', 'HON']
yahoo = Yahoo(repo=STOCK_REPO, dump_dir=None)
yahoo.reset(symbols, INFO_KEYS, price_start=None, price_end=DATE_END)

print("main.py done")