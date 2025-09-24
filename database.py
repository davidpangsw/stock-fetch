# pip3 install pymongo[srv]

from config import env
from stock_repository import StockRepositoryMongo, StockRepositoryMysql

DB_TYPE = env['DATABASE_TYPE']
if DB_TYPE == 'mongo':
    STOCK_REPO = StockRepositoryMongo(env['CONN_STR'], env['DATABASE'])
elif DB_TYPE == 'mysql':
    STOCK_REPO = StockRepositoryMysql(env['CONN_STR'], env['DATABASE'])
else:
    raise ValueError("Unknown database type")