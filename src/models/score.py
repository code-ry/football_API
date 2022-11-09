from init import db, ma
from marshmallow import fields

class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    winner = db.Column(db.String, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)

    team = db.relationship('Team', back_populates='scores')
    match = db.relationship('Match', back_populates='scores')

class ScoreSchema(ma.Schema):
    team = fields.Nested('TeamSchema', only=['name'])

    class Meta:
        fields= ('score', 'team', 'match_id')