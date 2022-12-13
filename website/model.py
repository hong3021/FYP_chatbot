from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Chatlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))
    answer = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(1000))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(150))
    chatlogs = db.relationship('Chatlog', backref='owner')
