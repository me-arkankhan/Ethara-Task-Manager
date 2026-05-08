from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role     = db.Column(db.String(10), nullable=False)  # 'Admin' or 'Member'
    tasks    = db.relationship('Task', backref='assignee', lazy=True)

class Task(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    status      = db.Column(db.String(20), default='Pending')  # Pending / Complete
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)