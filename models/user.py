from app import db
from models.ticket import Comment

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(50))    
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    admin = db.Column(db.Boolean())
    active = db.Column(db.Boolean())
    deleted = db.Column(db.Boolean)

    comments = db.relationship('Comment', backref='usercomments')


    
