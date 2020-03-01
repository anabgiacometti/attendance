from app import app
from flask import render_template, redirect, url_for, request, abort, session
from models.ticket import Ticket 

@app.route('/home')
def Home():
    if 'userid' not in session or session['userid'] == None:
        return redirect(url_for('Login'))

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

        return render_template('dashboard/index.html', admin=admin, tickets=tickets, count=count)
