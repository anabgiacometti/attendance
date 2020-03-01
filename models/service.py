from app import db

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float(precision=2))
    obs = db.Column(db.Text())
    deleted = db.Column(db.Boolean)

    
