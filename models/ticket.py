from app import db
from models.license import License

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(20))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    license_id = db.Column(db.Integer, db.ForeignKey('license.id'))
    date = db.Column(db.DateTime())
    status = db.Column(db.Integer())
    summary = db.Column(db.Text(100))
    problem = db.Column(db.Text())
    resolution = db.Column(db.Text())
    total_value = db.Column(db.Float(precision=2))
    is_warranty = db.Column(db.Boolean())
    responsable_tech = db.Column(db.String(100))    
    contact_name = db.Column(db.String(100))    
    obs = db.Column(db.Text())
    deleted = db.Column(db.Boolean())

    client = db.relationship('Client', backref='ticket_client')
    services = db.relationship('Service', secondary='ticket_services', backref='services', lazy='dynamic')
    license = db.relationship('License', backref='ticket_license')
    comments = db.relationship('Comment', backref='comments', order_by='Comment.date.desc()')
    files = db.relationship('TicketFile', backref='files')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime())
    comment = db.Column(db.Text())

    files = db.relationship('CommentFile', backref='files')
    user = db.relationship('User', backref='user')


class TicketFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    data = db.Column(db.LargeBinary())
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))
    deleted = db.Column(db.Boolean)


class CommentFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    data = db.Column(db.LargeBinary())
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    deleted = db.Column(db.Boolean)



db.Table('ticket_services', 
        db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.id')),
        db.Column('service_id', db.Integer, db.ForeignKey('service.id'))
    )
    




    
