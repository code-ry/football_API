from flask import Blueprint, request
from init import db
from models.match import Match, MatchSchema
from models.performance import  Performance, PerformanceSchema
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authorize

matches_bp = Blueprint('matches', __name__, url_prefix='/matches')

@matches_bp.route('/')
@jwt_required()
def all_matches():
    # selects all matches and orders by date attribute
    stmt = db.select(Match).order_by(Match.date.desc())
    matches = db.session.scalars(stmt).all()
    return MatchSchema(many=True).dump(matches)

@matches_bp.route('/<int:id>')
@jwt_required()
def one_match(id):
    # selects all matches and returns ones that match the id of input
    stmt = db.select(Match).filter_by(id=id)
    match = db.session.scalar(stmt)
    if match:
        return MatchSchema().dump(match)
    else:
        return {'error': f'match not found with id {id}'}, 404

@matches_bp.route('/', methods=['POST'])
@jwt_required()
def add_match():
    authorize()
    # retrieve data from incoming POST request and parse the JSON
    data = MatchSchema().load(request.json)
    # Creat new match model instance from the match_info
    match = Match(
        date = data['date'],
        location = data['location']
    )
    # Add and commit match to DB
    db.session.add(match)
    db.session.commit()
    # Respond to Client DB info and Successful creation Code 201
    return MatchSchema().dump(match), 201

@matches_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_match(id):
    authorize()
    # find the match
        # selects all matches and returns ones that match the id of input

    stmt = db.select(Match).filter_by(id=id)
    match = db.session.scalar(stmt)
    # if it exists, update it
    data = MatchSchema().load(request.json)
    if match:
        # use get method to retrieve data as it returns 'none' instead of exception.
        match.date = data.get('date') or match.date
        match.location = data.get('location') or match.location
        db.session.commit()
        return MatchSchema().dump(match)
    else:
        return {'error': f'match not found with id {id}'}, 404

@matches_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_match(id):
        # need admin status
    authorize()
    # selects all matches and returns ones that match the id of input

    stmt = db.select(Match).filter_by(id=id)
    match = db.session.scalar(stmt)
    if match:
        db.session.delete(match)
        db.session.commit()
        return {'message': f'match {match.id} deleted successfully'}
    else:
        return {'error': f'match not found with id {id}'}, 404

@matches_bp.route('/<int:id>/performances/')
@jwt_required()
def all_match_performances(id):
    # selects all performances that the match_id attribute equals the input value
    stmt = db.select(Performance).where(Performance.match_id == id)
    performances = db.session.scalars(stmt).all()

    return PerformanceSchema(many=True).dump(performances)