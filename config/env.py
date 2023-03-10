import os 

SECRET_KEY = os.environ['SECRET_KEY']
REFRESH_TOKEN_SECRET_KEY = os.environ['REFRESH_TOKEN_SECRET_KEY']

MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']
MYSQL_DATABASE = os.environ['MYSQL_DATABASE']
MYSQL_USER     = os.environ['MYSQL_USER']
MYSQL_HOST     = os.environ['MYSQL_HOST']
MYSQL_PORT     = os.environ['MYSQL_PORT']

TOKEN_REDIS_URL      = os.environ['TOKEN_REDIS_URL']
SIGNED_URL_REDIS_URL = os.environ['SIGNED_URL_REDIS_URL']