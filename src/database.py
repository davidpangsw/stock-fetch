# pip3 install pymongo[srv]
# Note: src expects lowercase host name

from stock_repository.stock_repository_mongo import StockRepositoryMongo
from stock_repository.stock_repository_mysql import StockRepositoryMysql
import os

env = os.environ
DB_TYPE = env['DATABASE_TYPE']
if DB_TYPE == 'mongo':
    STOCK_REPO = StockRepositoryMongo(env['CONN_STR'], env['DATABASE'])
elif DB_TYPE == 'mysql':
    STOCK_REPO = StockRepositoryMysql(env['CONN_STR'], env['DATABASE'])
else:
    raise ValueError(f"Unknown database type:[{DB_TYPE}]")