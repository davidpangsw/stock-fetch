from .stock_repository import StockRepository
import pymongo

class StockRepositoryMongo(StockRepository):
    def __init__(self, connStr, database):
        # print("connecting to ", connStr, database)
        self.client = pymongo.MongoClient(connStr)
        self.db = self.client[database]
        self.stocks = self.db['stocks']   # collection

    def create(self):
        pass  # no need to create in mongo db

    def get_stock(self, symbol, limit=20):
        result = list(self.stocks.find({'symbol': symbol}).limit(limit))
        print(result)
        return result

    def replace_one(self, doc):
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

    def insert_one(self, doc):
        result = self.stocks.insert_one(doc)
        return {
            # 'acknowledged': result.acknowledged,
            'inserted_id': result.inserted_id,
        }

    def insert_many(self, docs):
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
