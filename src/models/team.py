from init import db, ma
from marshmallow import fields

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String, nullable=False)
    wins = db.Column(db.Integer, nullable=False)
    ladder_pos = db.Column(db.String, nullable=False)

    players = db.relationship('Player', back_populates='team', cascade= 'all, delete')
    scores = db.relationship('Score', back_populates='team', cascade= 'all, delete')

class TeamSchema(ma.Schema):
    players = fields.List(fields.Nested('PlayerSchema', exclude=['team']))

    class Meta:
        fields = ('id', 'name', 'location', 'wins', 'ladder_pos', 'players')
