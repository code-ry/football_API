from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.user import User
from models.team import Team
from models.player import Player
from models.match import Match
from models.score import Score
from models.performance import Performance

db_commands_bp = Blueprint('db', __name__)

@db_commands_bp.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@db_commands_bp.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands_bp.cli.command('seed')
def seed_db():
    users = [
        User(
            name = 'Ryan Bussey',
            email = 'admin@football.com',
            password= bcrypt.generate_password_hash('afladmin').decode('utf-8'),
            is_admin = True
        ),
        User(
            name = 'Joe Blow',
            email = 'joeblow@gmail.com',
            password= bcrypt.generate_password_hash('12345').decode('utf-8')
        ),
    ]

    db.session.add_all(users)
    db.session.commit()
    print('Users seeded')

    teams = [
        Team(
            name = 'Dockers',
            location = 'Fremantle',
            wins = 4,
            ladder_pos = '1st'
        ),
        Team(
            name = 'Eagles',
            location = 'West Coast',
            wins = 0,
            ladder_pos = '18th'
        )
    ]

    db.session.add_all(teams)
    db.session.commit()
    print('Teams seeded')

    players = [
        Player(
            name = 'Nat Fyfe',
            age = 27,
            position = 'Midfield',
            team = teams[0]
        ),
        Player(
            name = 'Andy Brayshaw',
            age = 26,
            position = 'Midfield',
            team = teams[0]
        ),
        Player(
            name = 'Nic Natanui',
            age = 27,
            position = 'Ruck',
            team = teams[1]
        ),
        Player(
            name = 'Josh Kennedy',
            age = 26,
            position = 'Forward',
            team = teams[1]
        )
    ]

    db.session.add_all(players)
    db.session.commit()
    print('Players seeded')

    matches = [
        Match(
            date = '01/01/2022',
        ),
        Match(
            date = '05/06/2022',
        )
    ]

    db.session.add_all(matches)
    db.session.commit()
    print('Matches seeded')

    scores = [
        Score(
            score = 63,
            team = teams[0],
            match = matches[0]
        ),
        Score(
            score = 26,
            team = teams[1],
            match = matches[0]
        ),
        Score(
            score = 106,
            team = teams[0],
            match = matches[1]
        ),
        Score(
            score = 18,
            team = teams[1],
            match = matches[1]
        )
    ]

    db.session.add_all(scores)
    db.session.commit()
    print('Scores seeded')

    performances = [
        Performance(
            goals = 6,
            behinds = 5,
            disposals = 25,
            player = players[0],
            match = matches[0]
        ),
        Performance(
            goals = 5,
            behinds = 7,
            disposals = 30,
            player = players[0],
            match = matches[1]
        ),
    ]

    db.session.add_all(performances)
    db.session.commit()
    print('Performances seeded')