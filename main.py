from pathlib import Path
from yahoo import Yahoo

# DIR_DATA = './data'
DIR_DATA = None
INFO_KEYS = [
    'sector', 'industry',
    'country', 'exchange',
    'shortName', 'longName', 'symbol', 'market', 'marketCap',
    'longBusinessSummary', 'website',
]
NUMBER_OF_SYMBOLS = 999
DATE_END = "2025-09-23"     # end exclusive

def getSymbols(n=None):
    with open('symbols.txt') as file:
        lines = [line.rstrip() for line in file]
    with open('blacklist.txt') as file:
        blacklist = [line.rstrip() for line in file]
    
    lines = filter(lambda i: i not in blacklist, lines)
    lines = lines if n is None else list(lines)[0:n]
    return lines

symbols = getSymbols(NUMBER_OF_SYMBOLS)
# symbols = ['AAPL', 'HON']
yahoo = Yahoo(DIR_DATA)
yahoo.reset(symbols, INFO_KEYS, price_start=None, price_end=DATE_END)

print("main.py done")