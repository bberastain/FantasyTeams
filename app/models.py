from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from app import db, login
from flask_login import UserMixin
from time import time
import jwt
from flask import current_app
from hashlib import md5


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    pick = db.relationship('Pick', backref='author', lazy='dynamic')

# the backref creates a habit.author expression
# that returns the user given the habit

# what does lazy='dynamic' mean?
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer)
    away_id = db.Column(db.Integer)
    away_value = db.Column(db.Integer)
    home_id = db.Column(db.Integer)
    home_value = db.Column(db.Integer)
    winner_id = db.Column(db.Integer)


class Pick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer)
    team_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
