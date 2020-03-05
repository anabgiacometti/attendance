from app import app
from flask import render_template, redirect, url_for, request, abort, session
from models.ticket import Ticket 
from models.user import User
from models.client import Client
from models.warnings import Warning

@app.route('/home')
def Home():
    if 'userid' not in session or session['userid'] == None:
        return redirect(url_for('Login'))

    if 'client' in session and session['client'] != None: 
        return redirect(url_for('ClientDashboard'))

    else:
        admin = session['admin']
        tickets = Ticket.query.order_by(Ticket.date.desc()).limit(10).all()
        
        tickets_open = Ticket.query.filter(Ticket.status == 1).count()
        tickets_return = Ticket.query.filter(Ticket.status == 2).count()
        tickets_close = Ticket.query.filter(Ticket.status == 3).count()
        total = Ticket.query.count()
        if total == 0:
            total = 1

        count = {
            "open_percent": (tickets_open * 100) / total,
            "return_percent": (tickets_return * 100) / total,
            "close_percent": (tickets_close * 100) / total,
            "open": tickets_open, 
            "return": tickets_return, 
            "close": tickets_close, 
        }

        warnings = Warning.query.filter(Warning.user_id != session['userid']).filter(Warning.read == False).all()
        warning_ticket = []
        
        for w in warnings:
            warning_ticket.append(w.ticket_id)

        return render_template('dashboard/index.html', warnings=warning_ticket, admin=admin, tickets=tickets, count=count)

@app.route('/home/client')
def ClientDashboard():
    if 'userid' not in session or session['userid'] == None:
        return redirect(url_for('Login'))

    else:
        message = None

        if 'message' in session and session['message'] != None:
            message = session['message']
            session['message'] = None

        user = User.query.filter(User.id == session['userid']).first()
        name = user.name
        client = user.client

        q = request.args.get('q')
                
        if q:
            search = "{}".format(q)
            tickets = client.tickets.order_by(Ticket.date.desc())\
                .filter(Ticket.ticket_number == q)
        else:
            tickets = client.tickets
        
        tickets_open = Ticket.query.filter(Ticket.client_id == user.client_id).filter(Ticket.status == 1).count()
        tickets_return = Ticket.query.filter(Ticket.client_id == user.client_id).filter(Ticket.status == 2).count()
        tickets_close = Ticket.query.filter(Ticket.client_id == user.client_id).filter(Ticket.status == 3).count()
        total = Ticket.query.filter(Ticket.client_id == user.client_id).count()

        if total == 0:
            total = 1

        count = {
            "open_percent": (tickets_open * 100) / total,
            "return_percent": (tickets_return * 100) / total,
            "close_percent": (tickets_close * 100) / total,
            "open": tickets_open, 
            "return": tickets_return, 
            "close": tickets_close, 
        }

        warnings = Warning.query.filter(Warning.user_id != user.id).filter(Warning.read == False).all()
        warning_ticket = []
        
        for w in warnings:
            warning_ticket.append(w.ticket_id)

        return render_template('dashboard/index.html', warnings=warning_ticket, q=q, message=message, tickets=tickets, count=count, name=name, client=True)
