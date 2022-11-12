from flask import Blueprint, request
from init import db
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authorize

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/')
@jwt_required()
def all_users():
    authorize()
    # Selects all of users and returns them in order and if is admin
    stmt = db.select(User).order_by(User.is_admin , User.name)
    users = db.session.scalars(stmt).all()
    return UserSchema(many=True, exclude=['password']).dump(users)

@users_bp.route('/<int:id>/')
@jwt_required()
def one_user(id):
    authorize()
    # find the User, selects the User that has matching id to Input
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        return UserSchema(exclude=['password']).dump(user)
    else:
        return {'error': f'User not found with id {id}'}, 404

@users_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_User(id):
    authorize()
    # find the User, selects the User that has matching id to Input
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    # if it exists, update it
    data = UserSchema().load(request.json)
    if user:
        # use get method to retrieve data as it returns 'none' instead of exception.
        user.email = data.get('email') or user.email
        user.name = data.get('name') or user.name
        user.is_admin = data.get('is_admin') or user.is_admin
        db.session.commit()
        return UserSchema(exclude=['password']).dump(user)
    else:
        return {'error': f'User not found with id {id}'}, 404

@users_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_user(id):
    # need admin status
    authorize()
    # Selects the user matching the id from the input
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': f'User {user.name} deleted successfully'}
    else:
        return {'error': f'User not found with id {id}'}, 404

