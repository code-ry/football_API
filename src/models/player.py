from init import db, ma
from marshmallow import fields

class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
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

    class Meta:
        fields = ('id', 'name', 'age', 'height_cm', 'weight_kg', 'position', 'salary_per_year', 'team')
        ordered = True