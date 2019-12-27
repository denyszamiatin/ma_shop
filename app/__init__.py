from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from . import config

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from . import routes, models
