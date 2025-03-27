from api import app, db
from flask import abort, jsonify, request
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema
from marshmallow import ValidationError


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id: int):
    user = db.get_or_404(UserModel, user_id, description=f'User with id={user_id} not found')
    return jsonify(user_schema.dump(user)), 200


@app.route('/users', methods=['GET'])
def get_users():
    users_db = db.session.scalars(db.select(UserModel)).all()
    return jsonify(users_schema.dump(users_db)), 200


@app.route('/users', methods=['POST'])
def create_user():
    try:
        user = user_schema.loads(request.data)
        db.session.add(user)
        db.session.commit()
    except ValidationError as ve:
        abort(400, f'validation error: {str(ve)}')
    except Exception as e:
        db.session.rollback()
        abort(503, f'Database error: {str(e)}')
    return jsonify(user_schema.dump(user)), 201