from init import db, ma
from marshmallow import fields
from marshmallow.validate import Range

class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)

    team = db.relationship('Team', back_populates='scores')
    match = db.relationship('Match', back_populates='scores')

class ScoreSchema(ma.Schema):
    team = fields.Nested('TeamSchema', only=['name', 'id'])
    match = fields.Nested('MatchSchema', exclude=['scores'])
    team_id = fields.Integer(load_only=True)
    match_id = fields.Integer(load_only=True)

    # Validation
    score = fields.Integer(validate=Range(min=0, max=300))

    class Meta:
        fields= ('score', 'team', 'match', 'team_id', 'match_id')
        ordered = True