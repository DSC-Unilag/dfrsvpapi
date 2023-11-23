from flask import Flask
from config import config_options
from extensions import (
    ma, cors, db, migrate
)
from dotenv import load_dotenv
import os

load_dotenv()


def create_app(conf):
    app = Flask(__name__)
    app.config.from_object(config_options[conf])

    ma.init_app(app)
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from .views import rsvp
    app.register_blueprint(rsvp)

    return app
