from init import db, ma
from marshmallow import fields

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    home_ground = db.Column(db.String, nullable=False)
    wins = db.Column(db.Integer, nullable=False)
    losses = db.Column(db.Integer, nullable=False)
    ladder_position = db.Column(db.String, nullable=False)

    players = db.relationship('Player', back_populates='team', cascade= 'all, delete')
    scores = db.relationship('Score', back_populates='team', cascade= 'all, delete')

class TeamSchema(ma.Schema):
    players = fields.List(fields.Nested('PlayerSchema', only=['name', 'id', 'position']))

    class Meta:
        fields = ('id', 'name', 'home_ground', 'wins', 'losses', 'ladder_position' ,'players')
        ordered = True
