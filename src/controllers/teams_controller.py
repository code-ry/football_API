from flask import Blueprint, request
from init import db
from models.team import Team, TeamSchema
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authorize

teams_bp = Blueprint('teams', __name__, url_prefix='/teams')

@teams_bp.route('/')
@jwt_required()
def all_teams():
    stmt = db.select(Team).order_by(Team.name)
    teams = db.session.scalars(stmt).all()
    return TeamSchema(many=True).dump(teams)

@teams_bp.route('/<int:id>')
@jwt_required()
def one_team(id):
    stmt = db.select(Team).filter_by(id=id)
    team = db.session.scalar(stmt)
    if team:
        return TeamSchema().dump(team)
    else:
        return {'error': f'team not found with id {id}'}, 404

@teams_bp.route('/add/', methods=['POST'])
@jwt_required()
def auth_register():
    authorize()

    # retrieve data from incoming POST request and parse the JSON
    # Creat new team model instance from the team_info

    team = Team(
        name = request.json['name'],
        location = request.json['location'],
        wins  = request.json.get('wins'),
        ladder_pos =  request.json.get('ladder_pos')
    )
    # Add and commit team to DB
    db.session.add(team)
    db.session.commit()
    # Respond to Client DB info and Successful creation Code 201
    return TeamSchema().dump(team), 201

@teams_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_team(id):
    authorize()
    # find the team
    stmt = db.select(Team).filter_by(id=id)
    team = db.session.scalar(stmt)
    # if it exists, update it
    if team:
        # use get method to retrieve data as it returns 'none' instead of exception.
        team.name = request.json.get('name') or team.name
        team.location = request.json.get('location') or team.location
        team.ladder_pos = request.json.get('ladder_pos') or team.ladder_pos
        team.wins = request.json.get('wins') or team.wins
        db.session.commit()
        return TeamSchema().dump(team)
    else:
        return {'error': f'team not found with id {id}'}, 404

@teams_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_team(id):
        # need admin status
    authorize()

    stmt = db.select(Team).filter_by(id=id)
    team = db.session.scalar(stmt)
    if team:
        db.session.delete(team)
        db.session.commit()
        return {'message': f'team {team.name} deleted successfully'}
    else:
        return {'error': f'team not found with id {id}'}, 404

