from flask import Blueprint, request
from init import db
from models.performance import Performance, PerformanceSchema
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authorize

performances_bp = Blueprint('performances', __name__, url_prefix='/performances')

@performances_bp.route('/')
@jwt_required()
def all_performances():
    stmt = db.select(Performance).order_by(Performance.player_id)
    performances = db.session.scalars(stmt).all()
    return PerformanceSchema(many=True).dump(performances)

@performances_bp.route('/<int:id>')
@jwt_required()
def one_performance(id):
    stmt = db.select(Performance).filter_by(id=id)
    performance = db.session.scalar(stmt)
    if performance:
        return PerformanceSchema().dump(performance)
    else:
        return {'error': f'performance not found with id {id}'}, 404

@performances_bp.route('/', methods=['POST'])
@jwt_required()
def add_performance():
    authorize()

    # retrieve data from incoming POST request and parse the JSON
    # Creat new performance model instance from the performance_info

    performance = Performance(
        goals = request.json['goals'],
        behinds = request.json['behinds'],
        disposals = request.json['disposals'],
        injury = request.json['injury'],
        player_id = request.json['player_id'],
        match_id = request.json['match_id']
    )
    # Add and commit performance to DB
    db.session.add(performance)
    db.session.commit()
    # Respond to Client DB info and Successful creation Code 201
    return PerformanceSchema().dump(performance), 201

@performances_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_performance(id):
    authorize()
    # find the performance
    stmt = db.select(Performance).filter_by(id=id)
    performance = db.session.scalar(stmt)
    # if it exists, update it
    if performance:
        # use get method to retrieve data as it returns 'none' instead of exception.
        performance.goals = request.json.get('goals') or performance.goals
        performance.behinds = request.json.get('behinds') or performance.behinds
        performance.disposals = request.json.get('disposals') or performance.disposals
        performance.injury = request.json.get('injury') or performance.injury
        performance.player_id = request.json.get('player_id') or performance.player_id
        performance.match_id = request.json.get('match_id') or performance.match_id

        db.session.commit()
        return PerformanceSchema().dump(performance)
    else:
        return {'error': f'performance not found with id {id}'}, 404

@performances_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_performance(id):
        # need admin status
    authorize()

    stmt = db.select(Performance).filter_by(id=id)
    performance = db.session.scalar(stmt)
    if performance:
        db.session.delete(performance)
        db.session.commit()
        return {'message': f'performance {performance.id} deleted successfully'}
    else:
        return {'error': f'performance not found with id {id}'}, 404