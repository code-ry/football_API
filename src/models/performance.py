from init import db, ma

class Performance(db.Model):
    __tablename__ = 'performances'

    id = db.Column(db.Integer, primary_key=True)
    goals = db.Column(db.Integer, nullable=False)
    behinds = db.Column(db.Integer, nullable=False)
    disposals = db.Column(db.Integer, nullable=False)

    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)

    player = db.relationship('Player', back_populates='performances')
    match = db.relationship('Match', back_populates='performances')

class PerformanceSchema(ma.Schema):
    class Meta:
        fields= ('goals', 'behinds', 'disposals', 'player_id', 'match_id')