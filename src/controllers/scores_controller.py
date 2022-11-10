from flask import Blueprint, request
from init import db
from models.score import Score, ScoreSchema
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authorize

scores_bp = Blueprint('scores', __name__, url_prefix='/scores')

@scores_bp.route('/')
@jwt_required()
def all_scores():
    stmt = db.select(Score).order_by(Score.id)
    scores = db.session.scalars(stmt).all()
    return ScoreSchema(many=True).dump(scores)

@scores_bp.route('/<int:id>')
@jwt_required()
def one_score(id):
    stmt = db.select(Score).filter_by(id=id)
    score = db.session.scalar(stmt)
    if score:
        return ScoreSchema().dump(score)
    else:
        return {'error': f'score not found with id {id}'}, 404

@scores_bp.route('/', methods=['POST'])
@jwt_required()
def add_score():
    authorize()

    # retrieve data from incoming POST request and parse the JSON
    # Creat new score model instance from the score_info

    score = Score(
        score = request.json['score'],
        team_id = request.json['team_id'],
        match_id = request.json['match_id']
    )
    # Add and commit score to DB
    db.session.add(score)
    db.session.commit()
    # Respond to Client DB info and Successful creation Code 201
    return ScoreSchema().dump(score), 201

@scores_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_score(id):
    authorize()
    # find the score
    stmt = db.select(Score).filter_by(id=id)
    score = db.session.scalar(stmt)
    # if it exists, update it
    if score:
        # use get method to retrieve data as it returns 'none' instead of exception.
        score.score = request.json.get('score') or score.score
        score.team_id = request.json.get('team_id') or score.team_id
        score.match_id = request.json.get('match_id') or score.match_id

        db.session.commit()
        return ScoreSchema().dump(score)
    else:
        return {'error': f'score not found with id {id}'}, 404

@scores_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_score(id):
        # need admin status
    authorize()

    stmt = db.select(Score).filter_by(id=id)
    score = db.session.scalar(stmt)
    if score:
        db.session.delete(score)
        db.session.commit()
        return {'message': f'score {score.name} deleted successfully'}
    else:
        return {'error': f'score not found with id {id}'}, 404