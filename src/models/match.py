from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

class Match(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    location = db.Column(db.String, nullable=False)

    scores = db.relationship('Score', back_populates='match', cascade= 'all, delete')
    performances = db.relationship('Performance', back_populates='match', cascade= 'all, delete')

class MatchSchema(ma.Schema):
    scores = fields.List(fields.Nested('ScoreSchema', exclude=['match']))

    # Validation and Sanitation
    location = fields.String(validate=And(
        Length(min=1, max=50, error='location must be between 1 and 50 characters long'),
        Regexp('^[a-zA-Z ]+$', error='location must be only letters')))
    date = fields.String(validate=Regexp('(((0[1-9]|[12][0-9]|3[01])([/])(0[13578]|10|12)([/])(\d{4}))|(([0][1-9]|[12][0-9]|30)([/])(0[469]|11)([/])(\d{4}))|((0[1-9]|1[0-9]|2[0-8])([/])(02)([/])(\d{4}))|((29)(\.|-|\/)(02)([/])([02468][048]00))|((29)([/])(02)([/])([13579][26]00))|((29)([/])(02)([/])([0-9][0-9][0][48]))|((29)([/])(02)([/])([0-9][0-9][2468][048]))|((29)([/])(02)([/])([0-9][0-9][13579][26])))', error='date must be a valid date format dd/mm/yyyy'))

    class Meta:
        fields = ('id', 'date', 'location' ,'scores')