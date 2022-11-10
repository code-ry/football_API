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
            name = 'Fremantle Dockers',
            home_ground = 'Fremantle Oval',
            wins = 2,
            losses = 0,
            ladder_position = '1st'
        ),
        Team(
            name = 'West Coast Eagles',
            home_ground = 'Subiaco Oval',
            wins = 0,
            losses = 2,
            ladder_position = '3rd'
        ),
        Team(
            name = 'Geelong Cats',
            home_ground = 'The Cattery, GMHBA Stadium',
            wins = 1,
            losses = 1,
            ladder_position = '2nd'
        )
    ]

    db.session.add_all(teams)
    db.session.commit()
    print('Teams seeded')

    players = [
        Player(
            name = 'Nat Fyfe',
            age = 27,
            height_cm = 180,
            weight_kg = 85,
            salary_per_year = 150000,
            position = 'Midfield',
            team = teams[0]
        ),
        Player(
            name = 'Andy Brayshaw',
            age = 26,
            height_cm = 160,
            weight_kg = 63,
            salary_per_year = 200000,
            position = 'Midfield',
            team = teams[0]
        ),
        Player(
            name = 'Nic Natanui',
            age = 27,
            height_cm = 210,
            weight_kg = 106,
            salary_per_year = 180000,
            position = 'Ruck',
            team = teams[1]
        ),
        Player(
            name = 'Josh Kennedy',
            age = 26,
            height_cm = 196,
            weight_kg = 98,
            salary_per_year = 340000,
            position = 'Forward',
            team = teams[1]
        ),
        Player(
            name = 'Gary Ablett',
            age = 25,
            height_cm = 160,
            weight_kg = 75,
            salary_per_year = 400000,
            position = 'Half-Back',
            team = teams[2]
        ),
        Player(
            name = 'Tom Hawkins',
            age = 26,
            height_cm = 216,
            weight_kg = 112,
            salary_per_year = 185000,
            position = 'Forward',
            team = teams[2]
        )
    ]

    db.session.add_all(players)
    db.session.commit()
    print('Players seeded')

    matches = [
        Match(
            date = '01/01/2022',
            location = 'Fremantle Oval'
        ),
        Match(
            date = '05/06/2022',
            location = 'Subiaco Oval'
        ),
        Match(
            date = '01/08/2022',
            location = 'The Cattery, GMHBA Stadium'
        ),
        Match(
            date = '15/04/2022',
            location = 'The Cattery, GMHBA Stadium'
        )
    ]

    db.session.add_all(matches)
    db.session.commit()
    print('Matches seeded')

    scores = [
        Score(
            score = 63,
            team = teams[0],
            match = matches[0],
        ),
        Score(
            score = 26,
            team = teams[1],
            match = matches[0],
        ),
        Score(
            score = 106,
            team = teams[0],
            match = matches[1],
        ),
        Score(
            score = 18,
            team = teams[1],
            match = matches[1],
        ),
        Score(
            score = 96,
            team = teams[0],
            match = matches[2],
        ),
        Score(
            score = 95,
            team = teams[2],
            match = matches[2],
        ),
        Score(
            score = 50,
            team = teams[1],
            match = matches[3],
        ),
        Score(
            score = 10,
            team = teams[2],
            match = matches[3],
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
            injury = False,
            player = players[0],
            match = matches[0]
        ),
        Performance(
            goals = 5,
            behinds = 7,
            disposals = 30,
            injury = True,
            player = players[0],
            match = matches[1]
        ),
        Performance(
            goals = 1,
            behinds = 2,
            disposals = 4,
            injury = False,
            player = players[0],
            match = matches[2]
        ),
        Performance(
            goals = 5,
            behinds = 7,
            disposals = 30,
            injury = True,
            player = players[1],
            match = matches[1]
        ),
        Performance(
            goals = 6,
            behinds = 5,
            disposals = 25,
            injury = False,
            player = players[3],
            match = matches[3]
        ),
        Performance(
            goals = 5,
            behinds = 7,
            disposals = 30,
            injury = True,
            player = players[4],
            match = matches[2]
        )
    ]

    db.session.add_all(performances)
    db.session.commit()
    print('Performances seeded')