from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.user import User

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
            password= bcrypt.generate_password_hash('12345').decode('utf-8'),
        ),
    ]

    db.session.add_all(users)
    db.session.commit()
    print('Users seeded')