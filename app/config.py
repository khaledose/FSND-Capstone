import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.urandom(32)
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
    DB_USER = os.getenv('POSTGRES_USER',  'postgres')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', '123456789')
    DB_NAME = os.getenv('POSTGRES_DB_DEV', 'capstone_dev')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)) 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
