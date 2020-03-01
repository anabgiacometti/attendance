from app import db

class System(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    warranty = db.Column(db.Integer())
    obs = db.Column(db.Text())
    deleted = db.Column(db.Boolean)

    licenses = db.relationship('License', backref='system')



    
