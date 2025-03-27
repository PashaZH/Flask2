from passlib.apps import custom_app_context as pwd_context
from api import app, db
import sqlalchemy.orm as so
import sqlalchemy as sa
import jwt
from time import time







class UserModel(db.Model):
    __tablename__ = "users"


    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(32), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(128))

    def __init__(self, username, password):
        self.username = username
        self.hash_password(password)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
    
    def generate_auth_token(self):
        token = jwt.encode({'id': self.id, 'exp': int(time()+3600)},
                           key=app.config['SECRET_KEY'],
                           algorithm='HS256')
        return token
        # app.config['SECRET_KEY'] эквивалентно Config.SECRET_KEY

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms=['HS256'])
        except Exception as e:
            print(f'Error: {str(e)}')
            return None
        user = db.get_or_404(UserModel, data['id'])
        return user



