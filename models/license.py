from app import db
from models.client import Client
from models.system import System


class License(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    #DADOS DO SISTEMA
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    system_id = db.Column(db.Integer, db.ForeignKey('system.id'))
    date = db.Column(db.DateTime())
    instalation_tech = db.Column(db.String(100))
    seller = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    fabric_number = db.Column(db.String(100))
    training_tech = db.Column(db.String(100))
    training_client = db.Column(db.String(255))
    obs = db.Column(db.Text())
    deleted = db.Column(db.Boolean())

    client = db.relationship('Client', backref='client')
    files = db.relationship('LicenseFiles', backref='files')
    tickets = db.relationship('Ticket', backref='tickets')



class LicenseFiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    data = db.Column(db.LargeBinary())
    license_id = db.Column(db.Integer, db.ForeignKey('license.id'))
    deleted = db.Column(db.Boolean)

