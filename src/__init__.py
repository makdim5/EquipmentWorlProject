from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.errorhandler(404)
def not_found_error(error):
    return "Error 404", 404


@app.errorhandler(500)
def internal_error(error):
    return "Error 500", 500


db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

from . import routes
