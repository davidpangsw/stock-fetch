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
from abc import ABC, abstractmethod


class StockRepository(ABC):

    def __init__(self, connStr, database):
        pass

    def create(self):
        pass

    @abstractmethod
    def get_stock(self, symbol, limit=20):
        pass

    @abstractmethod
    def replace_one(self, doc):
        pass

    @abstractmethod
    def insert_one(self, doc):
        pass

    @abstractmethod
    def insert_many(self, docs):
        pass

    @abstractmethod
    def drop(self):
        pass



if __name__ == '__main__':
    # connStr = "mongodb://localhost:27017"
    # database = "myProjectDB"
    # repo = StockRepositoryMongo(connStr, database)

    connStr = "host=127.0.0.1;user=;password="
    database = "project"
    repo = StockRepositoryMysql(connStr, database)

