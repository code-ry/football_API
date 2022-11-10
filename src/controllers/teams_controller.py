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

@teams_bp.route('/', methods=['POST'])
@jwt_required()
def auth_register():
    authorize()

    # retrieve data from incoming POST request and parse the JSON
    # Creat new team model instance from the team_info

    team = Team(
        name = request.json['name'],
        home_ground = request.json['home_ground'],
        losses = request.json['losses'],
        wins  = request.json['wins'],
        ladder_position  = request.json['ladder_position']
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
        team.home_ground = request.json.get('home_ground') or team.home_ground
        team.losses = request.json.get('losses') or team.losses
        team.wins = request.json.get('wins') or team.wins
        team.ladder_position = request.json.get('ladder_position') or team.ladder_position
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

# @teams_bp.route('/<int:id>/matches/')
# @jwt_required()
# def all_teams_matches(id):

#     stmt = db.select(Match).where(Match.team_id == id)
#     matches = db.session.scalars(stmt).all()

#     return MatchSchema(many=True).dump(matches)

