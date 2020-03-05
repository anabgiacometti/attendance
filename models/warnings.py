from app import db

class Warning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    read = db.Column(db.Boolean)
    