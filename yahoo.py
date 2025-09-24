import json
import time
import yfinance as yf
from database import STOCK_REPO

class Yahoo:
    def __init__(self, dir):
        self.dir = dir;
    
    # def resetInfos(self, symbols, info_keys):
    #     tickers = yf.Tickers(symbols)
    #     lastUpdated = time.time()
    #     for symbol in symbols:
    #         print(f'symbol={symbol}')
    #         ticker = tickers.tickers[symbol.upper()]
    #         info = { key: ticker.info[key] if key in ticker.info else None for key in info_keys }
    #         info['lastUpdated'] = lastUpdated
    #         if self.dir is not None:
    #             json.dump(ticker.info, open(f'{self.dir}/info/raw/{symbol.lower()}.json', 'w')) # dump raw info
    #             json.dump(info, open(f'{self.dir}/info/{symbol.lower()}.json', 'w')) # dump custom info

    #         # save custom info to mongodb
    #         result = STOCK_REPO.replaceOneInfo(info)
    #         print(result)

    def reset(self, symbols, info_keys, price_start, price_end):
        STOCK_REPO.drop()
        STOCK_REPO.create()

        tickers = yf.Tickers(symbols)
        lastUpdated = time.time()

        for symbol in symbols:
            print(f'symbol={symbol}')
            try:
                ticker = tickers.tickers[symbol.upper()]
                stock = { key: ticker.info[key] if key in ticker.info else None for key in info_keys }
                # print(f'stock={stock}')
            except Exception as e:
                print(e)
                continue
            stock['prices'] = self.fetchPrices(symbol, price_start, price_end)
            stock['lastUpdated'] = lastUpdated
            if self.dir is not None:
                json.dump(ticker.info, open(f'{self.dir}/info/raw/{symbol.lower()}.json', 'w')) # dump raw info
                json.dump(stock, open(f'{self.dir}/stock/{symbol.lower()}.json', 'w')) # dump custom info
            
            result = STOCK_REPO.insertOne(stock)
            print(f'inserted symbol={symbol}; result={result}')
            stock.clear()
    
    def fetchPrices(self, symbol, start, end):
        df = yf.download([symbol], start=start, end=end, group_by='ticker')
        lastUpdated = time.time()
        # print(df)
        
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
            if count % 1000 == 0:
                print(count, item)
            count += 1
        if count == 0:
            print(f"Info: No prices for {symbol}")
        return items   # use yield?
