from flask import Flask
from init import db, bcrypt, ma, jwt
from controllers.cli_controller import db_commands_bp
from controllers.users_controller import users_bp
from controllers.auth_controller import auth_bp
from controllers.players_controller import players_bp
from controllers.teams_controller import teams_bp
from controllers.matches_controller import matches_bp
from controllers.scores_controller import scores_bp
from controllers.performances_controller import performances_bp
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError



import os

def create_app():
    app = Flask(__name__)

    app.config['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    db.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(db_commands_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(matches_bp)
    app.register_blueprint(scores_bp)
    app.register_blueprint(performances_bp)

    # When an expected body is received empty or wrong format
    @app.errorhandler(400)
    def not_found(err):
        return {"error" : str(err)}, 400
    # When a user fail to provide valid username/password
    @app.errorhandler(401)
    def unauthorized(err):
        return {"error" : str(err)}, 401
    # When a URL was not found on server
    @app.errorhandler(404)
    def not_found(err):
        return {"error" : str(err)}, 404
    # When a value is entered outside of range or invalid.
    @app.errorhandler(IntegrityError)
    def integrity_error(err):
        return {"error" : err.args}, 400
    # When a required field is not present.
    @app.errorhandler(KeyError)
    def key_error(err):
        return {"error" : f'The field {err} is required'}, 400
    # When an invalid input has been entered into a field.
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"error" : err.messages}, 400

    return app