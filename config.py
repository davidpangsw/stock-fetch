import os
from pathlib import Path
from dotenv import dotenv_values


env = dotenv_values(Path(".env"))
# if os.getenv('env') == 'production':
#     env = dotenv_values(Path(".env.prod"))
# else:
#     env = dotenv_values(Path(".env.dev"))
# print(f'env={env}')

# from dotenv import load_dotenv
# load_dotenv(dotenv_path=Path('./env/default'))
# def getConnectionString():
#     return os.getenv('CONN_STR')

# def getDatabase():
#     return os.getenv('DATABASE')