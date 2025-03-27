from api import ma
from api.models.user import UserModel
from marshmallow import validate, fields


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        exclude = ("password_hash",)
    
    username = ma.auto_field(required=True, validate=validate.Length(min=4))
    password = fields.Str(required=True, validate=validate.Length(min=5, max=15))


user_schema = UserSchema()
users_schema = UserSchema(many=True)