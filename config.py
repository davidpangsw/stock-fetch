import os
from dotenv import dotenv_values


env = dotenv_values(".env")
# if os.getenv('env') == 'production':
#     env = dotenv_values(".env.prod")
# else:
#     env = dotenv_values(".env.dev")
# print(f'env={env}')

# from dotenv import load_dotenv
# load_dotenv(dotenv_path='./env/default')
# def getConnectionString():
#     return os.getenv('CONN_STR')

# def getDatabase():
#     return os.getenv('DATABASE')