from init import db, ma
from marshmallow import fields, validates, ValidationError
from marshmallow.validate import Length, And, Regexp, Range, OneOf

VALID_POSITIONS = ('Full-Forward', 'Half-Forward', 'Midfield', 'Ruck', 'Half-Back', 'Full-Back')

class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height_cm = db.Column(db.Integer, nullable=False)
    weight_kg = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String, nullable=False)
    salary_per_year = db.Column(db.Integer, nullable=False)

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id') , nullable=False)

    team = db.relationship('Team', back_populates='players')
    performances = db.relationship('Performance', back_populates='player', cascade= 'all, delete')

class PlayerSchema(ma.Schema):
    team = fields.Nested('TeamSchema', only=['id', 'name'])

    # Validation
    name = fields.String(validate=And(
        Length(min=1, max=50, error='Name must be between 1 and 50 characters long'),
        Regexp('^[a-zA-Z ]+$', error='Name must be only letters')))
    age = fields.Integer(validate=Range(min=1, max=100))
    height_cm = fields.Integer(validate=Range(min=100, max=300))
    weight_kg = fields.Integer(validate=Range(min=20, max=300))
    position = fields.String(validate=OneOf(VALID_POSITIONS))
    salary_per_year = fields.Integer(validate=Range(min=1, max=2000000))

    @validates('name')
    def validate_status(self, value):
        # Check if name already exists
        stmt = db.select(Player).where(Player.name==value)
        player = db.session.scalar(stmt)
        # If player exists
        if player:
            raise ValidationError('You already have a player with that name.(If Updating record Omit "name" field')

    class Meta:
        fields = ('id', 'name', 'age', 'height_cm', 'weight_kg', 'position', 'salary_per_year', 'team', 'team_id')
        ordered = True