from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from ..Models import db

app = Flask(__name__)
CORS(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)