import json
import time
import yfinance as yf

INFO_KEYS = [
    'sector', 'industry',
    'country', 'exchange',
    'shortName', 'longName', 'symbol', 'market', 'marketCap',
    'longBusinessSummary', 'website',
]

class Yahoo:
    def __init__(self, repo, dump_dir):
        self.repo = repo
        self.dump_dir = dump_dir
    
    # def resetInfos(self, symbols, info_keys):
    #     tickers = yf.Tickers(symbols)
    #     lastUpdated = time.time()
    #     for symbol in symbols:
    #         print(f'symbol={symbol}')
    #         ticker = tickers.tickers[symbol.upper()]
    #         info = { key: ticker.info[key] if key in ticker.info else None for key in info_keys }
    #         info['lastUpdated'] = lastUpdated
    #         if self.dump_dir is not None:
    #             json.dump(ticker.info, open(f'{self.dump_dir}/info/raw/{symbol.lower()}.json', 'w')) # dump raw info
    #             json.dump(info, open(f'{self.dump_dir}/info/{symbol.lower()}.json', 'w')) # dump custom info

    #         # save custom info to mongodb
    #         result = self.repo.replace_one_info(info)
    #         print(result)

    def reset(self, symbols, price_start, price_end):
        self.repo.drop()
        self.repo.create()

        # symbols = ["VG"]
        # tickers = type('',(object,),{"tickers": {"VG": yf.Ticker("VG")}})()
        tickers = yf.Tickers(symbols)
        lastUpdated = time.time()

        for symbol in symbols:
            print(f'symbol={symbol}')
            try:
                ticker = tickers.tickers[symbol.upper()]
                stock = { key: ticker.info[key] if key in ticker.info else None for key in INFO_KEYS }
                # print(f'stock={stock}')
            except Exception as e:
                print(e)
                continue
            stock['prices'] = self.fetch_prices(symbol, price_start, price_end)
            stock['lastUpdated'] = lastUpdated
            if self.dump_dir is not None:
                json.dump(ticker.info, open(f'{self.dump_dir}/info/raw/{symbol.lower()}.json', 'w')) # dump raw info
                json.dump(stock, open(f'{self.dump_dir}/stock/{symbol.lower()}.json', 'w')) # dump custom info
            
            result = self.repo.insert_one(stock)
            # print(f'inserted symbol={symbol}; result={result}')
            stock.clear()
    
    def fetch_prices(self, symbol, start, end):
        df = yf.download([symbol], start=start, end=end, group_by='ticker', auto_adjust=True, progress=False)
        lastUpdated = time.time()
        # print(df)
        # flatten columns from ('AAPL', 'Open') to ('Open')
        # print(df.columns.tolist())
        df.columns = [f"{metric}" for ticker, metric in df.columns]
        # print(df.columns.tolist())
        
        count = 0
        items = []
        for date, row in df.iterrows():
            # print(row)
            item = {
                'date': date.timestamp(),
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'close': row['Close'],
                # 'close': row['Adj Close'],
                'volume': row['Volume'],
                'lastUpdated': lastUpdated,
            }
            if (item['open'] == 0): # 0 means None
                item['open'] = None
            items.append(item)

            # print(item)
            if count % 10000 == 0 and count > 0:
                print(count, item)
            count += 1
        if count == 0:
            print(f"Info: No prices for {symbol}")
        return items   # use yield?


"""
psycopg.errors.NotNullViolation: null value in column "longname" of relation "stocks" violates not-null constraint
DETAIL:  Failing row contains (289, null, VG, 2025-09-25 08:39:15).
"""