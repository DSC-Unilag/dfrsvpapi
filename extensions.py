from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass


ma = Marshmallow()
db = SQLAlchemy(model_class=Base)
migrate = Migrate()
cors = CORS()
