from init import db, ma
from marshmallow import fields, validates, ValidationError
from marshmallow.validate import Length, And, Regexp, Range, OneOf

VALID_LADDER_POSITIONS = ("1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th", "15th", "16th")

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    home_ground = db.Column(db.String, nullable=False)
    wins = db.Column(db.Integer, nullable=False)
    losses = db.Column(db.Integer, nullable=False)
    ladder_position = db.Column(db.String, nullable=False)

    players = db.relationship('Player', back_populates='team', cascade= 'all, delete')
    scores = db.relationship('Score', back_populates='team', cascade= 'all, delete')

class TeamSchema(ma.Schema):
    players = fields.List(fields.Nested('PlayerSchema', only=['name', 'id', 'position']))

    # Validation and Sanitation
    name = fields.String(validate=And(
        Length(min=1, max=50, error='Name must be between 1 and 50 characters long'),
        Regexp('^[a-zA-Z ]+$', error='Name must be only letters')))
    home_ground = fields.String(validate=And(
        Length(min=1, max=50, error='home_ground must be between 1 and 50 characters long'),
        Regexp('^[a-zA-Z ]+$', error='home_ground must be only letters')))
    wins = fields.Integer(validate=Range(min=0, max=30))
    losses = fields.Integer(validate=Range(min=0, max=30))
    ladder_position = fields.String(validate=OneOf(VALID_LADDER_POSITIONS))

    @validates('name')
    def validate_status(self, value):
        # Check if name already exists
        stmt = db.select(Team).where(Team.name==value)
        player = db.session.scalar(stmt)
        # If player exists
        if player:
            raise ValidationError('You already have a team with that name.(If Updating record Omit "name" field')
    
    @validates('ladder_position')
    def validate_status(self, value):
        # Check if name already exists
        stmt = db.select(Team).where(Team.ladder_position==value)
        team = db.session.scalar(stmt)
        # If Team exists
        if team:
            raise ValidationError('You already have a team with that ladder position.(If Updating record Omit "ladder_position" field')

    class Meta:
        fields = ('id', 'name', 'home_ground', 'wins', 'losses', 'ladder_position' ,'players')
        ordered = True
