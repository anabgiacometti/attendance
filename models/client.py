from app import db

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer())
    
    #DADOS DA EMPRESA
    cnpj = db.Column(db.String(100))
    cpf = db.Column(db.String(100))
    bussiness_name = db.Column(db.String(100))
    company_name = db.Column(db.String(100))
    state_number = db.Column(db.String(100))    

    #ENDEREÇO
    zip_code = db.Column(db.String(100))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    district = db.Column(db.String(100))
    address = db.Column(db.String(100))
    number = db.Column(db.String(100))
    addicional_info = db.Column(db.String(100))

    #DADOS DE CONTATO
    contact = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_2 = db.Column(db.String(100))
    
    obs = db.Column(db.Text())
    deleted = db.Column(db.Boolean)

    licenses = db.relationship('License', backref='license')
    tickets = db.relationship('Ticket', backref='ticket', lazy='dynamic')

    
