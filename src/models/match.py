from init import db

class Match(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)

    scores = db.relationship('Score', back_populates='match', cascade= 'all, delete')
    performances = db.relationship('Performance', back_populates='match', cascade= 'all, delete')