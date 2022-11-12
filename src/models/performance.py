from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, Range

class Performance(db.Model):
    __tablename__ = 'performances'

    id = db.Column(db.Integer, primary_key=True)
    goals = db.Column(db.Integer, nullable=False)
    behinds = db.Column(db.Integer, nullable=False)
    disposals = db.Column(db.Integer, nullable=False)
    injuries = db.Column(db.String, nullable=True)

    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)

    player = db.relationship('Player', back_populates='performances')
    match = db.relationship('Match', back_populates='performances')

class PerformanceSchema(ma.Schema):
    player = fields.Nested('PlayerSchema', only=['name','id'])
    match = fields.Nested('MatchSchema', only=['date','id','location'])

    # Validation and Sanitation
    goals = fields.Integer(validate=Range(min=0, max=20))
    behinds = fields.Integer(validate=Range(min=0, max=20))
    disposals = fields.Integer(validate=Range(min=0, max=100))
    injuries = fields.String(load_default='None',validate=And(
        Length(min=1, max=100, error='Injury description must be between 1 and 100 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Injury must be only letters and numbers')))
    player_id = fields.Integer(load_only=True)
    match_id = fields.Integer(load_only=True)
    
    class Meta:
        fields= ('id', 'player', 'match', 'goals', 'behinds', 'disposals', 'injuries','player_id','match_id')
        ordered = True