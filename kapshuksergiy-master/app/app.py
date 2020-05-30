from flask import Flask

from .alch_class import Base, engine
from .config import Configuration
import flask.logging


app = Flask(__name__)
logger = flask.logging.create_logger(app)
app.config.from_object(Configuration)
Base.metadata.create_all(bind=engine)

