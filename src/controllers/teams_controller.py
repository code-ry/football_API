from flask import Blueprint, request
from init import db
from models.team import Team, TeamSchema
from models.match import Match, MatchSchema
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authorize

teams_bp = Blueprint('teams', __name__, url_prefix='/teams')

@teams_bp.route('/')
@jwt_required()
def all_teams():
    #  Selects all of Team entities returns them by order of their name attribute
    stmt = db.select(Team).order_by(Team.name)
    teams = db.session.scalars(stmt).all()
    return TeamSchema(many=True).dump(teams)

@teams_bp.route('/<int:id>')
@jwt_required()
def one_team(id):
    # Filters out all teams with team.id matching the input field in argument.
    # returns single team entity
    stmt = db.select(Team).filter_by(id=id)
    team = db.session.scalar(stmt)
    if team:
        return TeamSchema().dump(team)
    else:
        return {'error': f'team not found with id {id}'}, 404

@teams_bp.route('/', methods=['POST'])
@jwt_required()
def auth_register():
    authorize()

    # retrieve data from incoming POST request and parse the JSON
    data = TeamSchema().load(request.json)
    # Creat new team model instance from the team_info
    team = Team(
        name = data['name'],
        home_ground = data['home_ground'],
        losses = data['losses'],
        wins  = data['wins'],
        ladder_position  = data['ladder_position']
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
    # Filters out all teams with team.id matching the input field in argument.
    # returns single team entity
    stmt = db.select(Team).filter_by(id=id)
    team = db.session.scalar(stmt)
    # if it exists, update it
    data = TeamSchema().load(request.json)
    if team:
        # use get method to retrieve data as it returns 'none' instead of exception.
        team.name = data.get('name') or team.name
        team.home_ground = data.get('home_ground') or team.home_ground
        team.losses = data.get('losses') or team.losses
        team.wins = data.get('wins') or team.wins
        team.ladder_position = data.get('ladder_position') or team.ladder_position
        db.session.commit()
        return TeamSchema().dump(team)
    else:
        return {'error': f'team not found with id {id}'}, 404

@teams_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_team(id):
        # need admin status
    authorize()
    # Filters out all teams with team.id matching the input field in argument.
    # returns single team entity
    stmt = db.select(Team).filter_by(id=id)
    team = db.session.scalar(stmt)
    if team:
        db.session.delete(team)
        db.session.commit()
        return {'message': f'team {team.name} deleted successfully'}
    else:
        return {'error': f'team not found with id {id}'}, 404


