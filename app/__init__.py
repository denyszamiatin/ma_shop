from flask import Flask
from flask_bootstrap import Bootstrap
from . import config

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(config.Config)

from . import routes
