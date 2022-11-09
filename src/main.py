from flask import Flask
from init import db, bcrypt, ma
from controllers.cli_controller import db_commands_bp
from controllers.users_controller import users_bp
import os

def create_app():
    app = Flask(__name__)

    app.config['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    db.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)


    app.register_blueprint(db_commands_bp)
    app.register_blueprint(users_bp)


    return app