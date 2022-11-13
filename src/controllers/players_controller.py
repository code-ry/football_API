from flask import Blueprint, request
from init import db
from models.player import Player, PlayerSchema
from models.performance import Performance, PerformanceSchema
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authorize

players_bp = Blueprint('players', __name__, url_prefix='/players')

@players_bp.route('/')
@jwt_required()
def all_players():
    # Selects all of Player entities and returns them in order of name
    stmt = db.select(Player).order_by(Player.name)
    players = db.session.scalars(stmt).all()
    return PlayerSchema(many=True, exclude=['team_id']).dump(players)

@players_bp.route('/<int:id>')
@jwt_required()
def one_player(id):
    # Filters out all Player with player.id matching the input field in argument.
    # returns single player entity
    stmt = db.select(Player).filter_by(id=id)
    player = db.session.scalar(stmt)
    if player:
        return PlayerSchema().dump(player)
    else:
        return {'error': f'player not found with id {id}'}, 404

@players_bp.route('/', methods=['POST'])
@jwt_required()
def add_player():
    authorize()

    # retrieve data from incoming POST request and parse the JSON
    data = PlayerSchema().load(request.json)
    # Creat new player model instance from the data
    player = Player(
        name = data['name'],
        age = data['age'],
        height_cm = data['height_cm'],
        weight_kg = data['weight_kg'],
        salary_per_year = data['salary_per_year'],
        position  = data['position'],
        team_id =  data['team_id']
    )
    # Add and commit player to DB
    db.session.add(player)
    db.session.commit()
    # Respond to Client DB info and Successful creation Code 201
    return PlayerSchema().dump(player), 201

@players_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_player(id):
    authorize()
    # Filters out all Player with player.id matching the input field in argument.
    # returns single player entity
    stmt = db.select(Player).filter_by(id=id)
    player = db.session.scalar(stmt)
    # if it exists, update it
    data = PlayerSchema().load(request.json)
    if player:
        # use get method to retrieve data as it returns 'none' instead of exception.
        player.name = data.get('name') or player.name
        player.height_cm = data.get('height_cm') or player.height_cm
        player.age = data.get('age') or player.age
        player.weight_kg = data.get('weight_kg') or player.weight_kg
        player.salary_per_year = data.get('salary_per_year') or player.salary_per_year
        player.position = data.get('position') or player.position
        player.team_id = data.get('team_id') or player.team_id
        db.session.commit()
        return PlayerSchema().dump(player)
    else:
        return {'error': f'player not found with id {id}'}, 404

@players_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_player(id):
        # need admin status
    authorize()
    # Filters out all Player with player.id matching the input field in argument.
    # returns single player entity
    stmt = db.select(Player).filter_by(id=id)
    player = db.session.scalar(stmt)
    if player:
        db.session.delete(player)
        db.session.commit()
        return {'message': f'player {player.name} deleted successfully'}
    else:
        return {'error': f'player not found with id {id}'}, 404
    
@players_bp.route('/<int:id>/performances/')
@jwt_required()
def all_players_performances(id):
    # selects all Performance entities that the player_id value attribute matches the input value in the argument
    # returns all matching Performance entities
    stmt = db.select(Performance).where(Performance.player_id == id)
    performances = db.session.scalars(stmt).all()

    return PerformanceSchema(many=True).dump(performances)
