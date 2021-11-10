from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from .config import DB_PATH, SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy()

def setup_db(app):
    db.app = app
    db.init_app(app)
    Migrate(app, db)