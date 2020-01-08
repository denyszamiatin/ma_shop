from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from app import config

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)


from . import routes, models
