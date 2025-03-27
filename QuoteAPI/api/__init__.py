from flask import Flask, g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Solution
# https://stackoverflow.com/questions/59455520/flask-sqlalchemy-marshmallow-error-on-relationship-one-to-many
migrate = Migrate(app, db)
ma = Marshmallow(app)
ma.init_app(app)
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)



@basic_auth.verify_password
def verify_password(username, password):
    from api.models.user import UserModel
    user = db.one_or_404(db.select(UserModel).filter_by(username=username))
    if not user or not user.verify_password(password):
        return False
    # g - специальный класс flask, который хранит контекст нашего приложения
    # нашего пользователя мы добавляем к глобальному контексту приложения
    g.user = user
    return True


@token_auth.verify_token
def verify_token(token):
   from api.models.user import UserModel
   user = UserModel.verify_auth_token(token)
   print(f"{user=}")
   return user



from api.handlers import author
from api.handlers import quote
from api.handlers import user
from api.handlers import token