# Repository style
#
# Validate data:
# SELECT * FROM stock_prices p1
# LEFT JOIN (
#     SELECT stock_id, MAX(date) AS md FROM `stock_prices`
#     WHERE open IS NULL GROUP BY stock_id
# ) p ON p1.stock_id = p.stock_id
# WHERE p1.date <= p.md
# AND p1.open IS NOT NULL
# AND p1.volume != 0;
#
import pymongo
import mysql.connector
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


class StockRepository(ABC):

    def __init__(self, connStr, database):
        pass

    def create(self):
        pass

    @abstractmethod
    def getStock(self, symbol, limit=20):
        pass

    @abstractmethod
    def replaceOne(self, doc):
        pass

    @abstractmethod
    def insertOne(self, doc):
        pass

    @abstractmethod
    def insertMany(self, docs):
        pass

    @abstractmethod
    def drop(self):
        pass


class StockRepositoryMongo(StockRepository):
    def __init__(self, connStr, database):
        # print("connecting to ", connStr, database)
        self.client = pymongo.MongoClient(connStr)
        self.db = self.client[database]
        self.stocks = self.db['stocks']   # collection

    def create(self):
        pass  # no need to create in mongo db

    def getStock(self, symbol, limit=20):
        result = list(self.stocks.find({'symbol': symbol}).limit(limit))
        print(result)
        return result

    def replaceOne(self, doc):
        result = self.stocks.replace_one(
            {'symbol': doc['symbol']}, doc, upsert=True)
        # See ReplaceOneResult
        return {
            # 'acknowledged': result.acknowledged,
            'matched_count': result.matched_count,
            'modified_count': result.modified_count,   # 0 if insert
            # 'raw_result': result.raw_result,
            'upserted_id': result.upserted_id,         # None if update
        }

    def insertOne(self, doc):
        result = self.stocks.insert_one(doc)
        return {
            # 'acknowledged': result.acknowledged,
            'inserted_id': result.inserted_id,
        }

    def insertMany(self, docs):
        result = self.stocks.insert_many(docs)
        # See InsertManyResult
        return {
            # 'acknowledged': result.acknowledged,
            # 'inserted_ids': result.inserted_ids ,
            'len(inserted_ids)': len(result.inserted_ids)
        }

    def drop(self):
        success = self.stocks.drop()
        return {
            'success': success,
        }

    # def replaceStockPrice(self, doc):
    #     query = {'symbol': doc['symbol'], 'date': doc['date']}
    #     # print(query)
    #     result = self.prices.replace_one(query, doc, upsert=True)
    #     return {
    #         # 'acknowledged': result.acknowledged,
    #         'matched_count': result.matched_count,
    #         'modified_count': result.modified_count,   # 0 if insert
    #         # 'raw_result': result.raw_result,
    #         'upserted_id': result.upserted_id,         # None if update
    #     }


class StockRepositoryMysql(StockRepository):
    # https://blog.devart.com/mysql-data-types.html
    CREATE_STOCK_QUERY = """
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            longName VARCHAR(255) NOT NULL,
            symbol VARCHAR(15) UNIQUE NOT NULL,
            lastUpdated DATETIME NOT NULL
        );
        CREATE TABLE IF NOT EXISTS stock_prices (
            stock_id INTEGER NOT NULL,
            date DATETIME NOT NULL,
            open DOUBLE, -- allow NULL
            high DOUBLE NOT NULL,
            low DOUBLE NOT NULL,
            close DOUBLE NOT NULL,
            volume BIGINT UNSIGNED NOT NULL,

            PRIMARY KEY(stock_id, date),
            FOREIGN KEY fk_stock_prices_stocks_stock_id (stock_id) REFERENCES stocks (id) ON DELETE CASCADE
        );
    """

    DROP_STOCK_QUERY = """
        DELETE FROM stock_prices;
        DELETE FROM stocks;
        -- DROP TABLE IF EXISTS stock_prices;
        -- DROP TABLE IF EXISTS stocks;
    """

    def __init__(self, connStr, database):
        params = dict(entry.split('=') for entry in connStr.split(';'))
        # print("connecting to ", connStr, params, database)
        params['database'] = database
        self.conn = mysql.connector.connect(**params)

        # ping
        self.conn.ping()
        # cursor = self.conn.cursor()
        # cursor.execute("SHOW DATABASES")
        # for row in cursor.fetchall():
        #     print(row)

    def create(self):
        cursor = self.cursor()
        cursor.execute(self.CREATE_STOCK_QUERY)

    def cursor(self):
        self.conn.reconnect()
        return self.conn.cursor()

    def timestampToString(self, timestamp):
        if timestamp < 0:
            dt = datetime.utcfromtimestamp(0) + timedelta(seconds=timestamp)
        else:
            dt = datetime.utcfromtimestamp(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    def getStock(self, symbol, limit=20):
        cursor = self.cursor()
        cursor.execute("""
        SELECT * FROM stocks
        WHERE symbol=%(symbol)s
        LIMIT %(limit)d
        """, {
            'symbol': symbol,
            'limit': limit,
        })
        result = [row for row in cursor.fetchall()]
        # result = list(self.stocks.find({'symbol': symbol}).limit(limit))
        # print(result)
        return result

    def replaceOne(self, doc):
        raise NotImplementedError()

    def insertOne(self, doc):
        prices = doc['prices']

        cursor = self.cursor()
        cursor.execute(
            """
            INSERT IGNORE INTO stocks (longName, symbol, lastUpdated)
            VALUES (%(longName)s, %(symbol)s, %(lastUpdated)s)
            """,
            {
                "longName": doc['longName'],
                "symbol": doc['symbol'],
                "lastUpdated": self.timestampToString(doc['lastUpdated']),
            })
        stockId = cursor.lastrowid

        BATCH_SIZE = 1000
        for i in range(0, len(prices), BATCH_SIZE):
            batch = prices[i:min(i + BATCH_SIZE, len(prices))]
            cursor.executemany(
                """
                INSERT IGNORE INTO stock_prices (stock_id, date,
                                        open, high, low, close, volume)
                VALUES (%(stock_id)s, %(date)s,
                        %(open)s, %(high)s, %(low)s, %(close)s, %(volume)s
                        )
                """,
                [{
                    'stock_id': stockId,
                    'date': self.timestampToString(price['date']),
                    'open': price['open'],
                    'high': price['high'],
                    'low': price['low'],
                    'close': price['close'],
                    'volume': price['volume'],
                } for price in batch]
            )
        self.conn.commit()
        return {
            'inserted_id': stockId,
        }

    def insertMany(self, docs):
        raise NotImplementedError()

    def drop(self):
        self.cursor().execute(self.DROP_STOCK_QUERY)
        return {
            'success': True,
        }


if __name__ == '__main__':
    # connStr = "mongodb://localhost:27017"
    # database = "myProjectDB"
    # repo = StockRepositoryMongo(connStr, database)

    connStr = "host=127.0.0.1;user=;password="
    database = "project"
    repo = StockRepositoryMysql(connStr, database)

