from flask import Blueprint, request, abort
from init import db, bcrypt
from models.user import User, UserSchema
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def authorize():
    user_id = get_jwt_identity()
    # Filters out all User entities with user.id matching the input field in argument.
    # returns single user entity
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user.is_admin:
        abort(401)

@auth_bp.route('/register/', methods=['POST'])
def auth_register():
    try:
        # Retrieve data from incoming POST request and parse the JSON
        data = UserSchema().load(request.json)
        # Create new user model instance from the user_info
        user = User(
            email = data['email'],
            password = bcrypt.generate_password_hash(data['password']).decode('utf-8'),
            name  = data.get('name')
        )
        # Add and commit user to DB
        db.session.add(user)
        db.session.commit()
        # Respond to Client DB info and Successful creation Code 201
        return UserSchema(exclude=['password']).dump(user), 201

    except IntegrityError:
        return {'error':'Email address already in use'}, 409

@auth_bp.route('/login/', methods = ['POST'])
def auth_login():

    # Filters out all User entities with user.email matching the input field in request body.
    # returns single user entity
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)
    
    if user and bcrypt.check_password_hash(user.password,request.json['password']):
        # create token for client to store and use.
        token = create_access_token(identity= str(user.id), expires_delta=timedelta(days=1))
        return {'user': user.email, 'token': token, 'is_admin': user.is_admin}
    else:
        return {'error': 'Invalid email or password'}, 401