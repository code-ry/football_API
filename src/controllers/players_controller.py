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

    stmt = db.select(Player).order_by(Player.name)
    players = db.session.scalars(stmt).all()
    return PlayerSchema(many=True).dump(players)

@players_bp.route('/<int:id>')
@jwt_required()
def one_player(id):
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
    # player_info = playerSchema().load(request.json)
    # Creat new player model instance from the player_info

    player = Player(
        name = request.json['name'],
        age = request.json['age'],
        height_cm = request.json['height_cm'],
        weight_kg = request.json['weight_kg'],
        salary_per_year = request.json['salary_per_year'],
        position  = request.json.get('position'),
        team_id =  request.json.get('team_id')
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
    # find the player
    stmt = db.select(Player).filter_by(id=id)
    player = db.session.scalar(stmt)
    # if it exists, update it
    if player:
        # use get method to retrieve data as it returns 'none' instead of exception.
        player.name = request.json.get('name') or player.name
        player.height_cm = request.json.get('height_cm') or player.height_cm
        player.age = request.json.get('age') or player.age
        player.weight_kg = request.json.get('weight_kg') or player.weight_kg
        player.salary_per_year = request.json.get('salary_per_year') or player.salary_per_year
        player.position = request.json.get('position') or player.position
        player.team_id = request.json.get('team_id') or player.team_id
        db.session.commit()
        return PlayerSchema().dump(player)
    else:
        return {'error': f'player not found with id {id}'}, 404

@players_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_player(id):
        # need admin status
    authorize()

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

    stmt = db.select(Performance).where(Performance.player_id == id)
    performances = db.session.scalars(stmt).all()

    return PerformanceSchema(many=True).dump(performances)
