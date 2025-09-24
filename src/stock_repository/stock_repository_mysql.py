from .stock_repository import StockRepository
import mysql.connector
from datetime import datetime, timedelta
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

    def timestamp_to_string(self, timestamp):
        if timestamp < 0:
            dt = datetime.utcfromtimestamp(0) + timedelta(seconds=timestamp)
        else:
            dt = datetime.utcfromtimestamp(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    def get_stock(self, symbol, limit=20):
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

    def replace_one(self, doc):
        raise NotImplementedError()

    def insert_one(self, doc):
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
                "lastUpdated": self.timestamp_to_string(doc['lastUpdated']),
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
                    'date': self.timestamp_to_string(price['date']),
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

    def insert_many(self, docs):
        raise NotImplementedError()

    def drop(self):
        self.cursor().execute(self.DROP_STOCK_QUERY)
        return {
            'success': True,
        }
