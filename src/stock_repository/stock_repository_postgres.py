from .stock_repository import StockRepository
import psycopg
from datetime import datetime, timedelta

class StockRepositoryPostgres(StockRepository):
    CREATE_STOCK_QUERY = """
        CREATE TABLE IF NOT EXISTS stocks (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            shortName VARCHAR(255),
            longName VARCHAR(255),
            symbol VARCHAR(15) UNIQUE NOT NULL,
            lastUpdated TIMESTAMP NOT NULL
        );

        CREATE TABLE IF NOT EXISTS stock_prices (
            stock_id INTEGER NOT NULL,
            date TIMESTAMP NOT NULL,
            open DOUBLE PRECISION,
            high DOUBLE PRECISION NOT NULL,
            low DOUBLE PRECISION NOT NULL,
            close DOUBLE PRECISION NOT NULL,
            volume BIGINT NOT NULL,

            PRIMARY KEY(stock_id, date),
            FOREIGN KEY (stock_id) REFERENCES stocks (id) ON DELETE CASCADE
        );
    """

    DROP_STOCK_QUERY = """
        DROP TABLE IF EXISTS stock_prices;
        DROP TABLE IF EXISTS stocks;
    """

    def __init__(self, connStr, database=None):
        # PostgreSQL uses space-separated or URI-style connection strings
        self.conn = psycopg.connect(connStr)

    def create(self):
        with self.conn.cursor() as cursor:
            cursor.execute(self.CREATE_STOCK_QUERY)
        self.conn.commit()

    def cursor(self):
        return self.conn.cursor()

    def timestamp_to_string(self, timestamp):
        if timestamp < 0:
            dt = datetime.utcfromtimestamp(0) + timedelta(seconds=timestamp)
        else:
            dt = datetime.utcfromtimestamp(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    def get_stock(self, symbol, limit=20):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM stocks
                WHERE symbol = %(symbol)s
                LIMIT %(limit)s
            """, {
                'symbol': symbol,
                'limit': limit
            })
            return cursor.fetchall()

    def replace_one(self, doc):
        raise NotImplementedError()

    def insert_one(self, doc):
        prices = doc['prices']

        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO stocks (name, shortName, longName, symbol, lastUpdated)
                VALUES (%(name)s, %(shortName)s, %(longName)s, %(symbol)s, %(lastUpdated)s)
                ON CONFLICT (symbol) DO NOTHING
                RETURNING id;
                """,
                {
                    "name": doc.get('longName') if doc.get('longName') is not None else doc.get('shortName', None),
                    "shortName": doc.get('shortName', None),
                    "longName": doc.get('longName', None),
                    "symbol": doc['symbol'],
                    "lastUpdated": self.timestamp_to_string(doc['lastUpdated']),
                }
            )

            result = cursor.fetchone()
            if result:
                stock_id = result[0]
            else:
                # If already exists, get the id
                cursor.execute("SELECT id FROM stocks WHERE symbol = %s", (doc['symbol'],))
                stock_id = cursor.fetchone()[0]

            BATCH_SIZE = 1000
            for i in range(0, len(prices), BATCH_SIZE):
                batch = prices[i:i + BATCH_SIZE]
                cursor.executemany(
                    """
                    INSERT INTO stock_prices (
                        stock_id, date, open, high, low, close, volume
                    ) VALUES (
                        %(stock_id)s, %(date)s, %(open)s, %(high)s,
                        %(low)s, %(close)s, %(volume)s
                    )
                    ON CONFLICT (stock_id, date) DO NOTHING
                    """,
                    [{
                        'stock_id': stock_id,
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
            'inserted_id': stock_id
        }

    def insert_many(self, docs):
        raise NotImplementedError()

    def drop(self):
        with self.conn.cursor() as cursor:
            cursor.execute(self.DROP_STOCK_QUERY)
        self.conn.commit()
        return {
            'success': True
        }
