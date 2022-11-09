from init import db

class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)

    team = db.relationship('Team', back_populates='scores')
    match = db.relationship('Match', back_populates='scores')