from init import db

class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String, nullable=False)

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id') , nullable=False)

    team = db.relationship('Team', back_populates='players')
    performances = db.relationship('Performance', back_populates='player', cascade= 'all, delete')