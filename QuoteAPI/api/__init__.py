from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_marshmallow import Marshmallow


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(model_class=Base)
db.init_app(app)

migrate = Migrate(app, db)
ma = Marshmallow(app)
ma.init_app(app)


from api.handlers import author
from api.handlers import quote
from api.handlers import user