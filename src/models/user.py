from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, Email

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class UserSchema(ma.Schema):

    # Validation
    name = fields.String(validate=And(
        Length(min=1, max=50, error='Name must be between 1 and 50 characters long'),
        Regexp('^[a-zA-Z ]+$', error='Name must be only letters')))
    email = fields.String(validate=Email())
    password = fields.String(validate=And(
        Length(min=8, max=20, error='Password must be between 8 and 20 characters long'),
        Regexp('(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)', error='Password must contain an UpperCase letter, Lowercase letter, number and symbol')))

    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin')
        ordered = True


