from app import app, db
from models.ticket import CommentFile, Ticket, Comment, TicketFile
from models.client import Client
from models.license import License
from models.service import Service 
from models.system import System
from flask import render_template, redirect, url_for, request, abort, session, jsonify, send_file
from flask_paginate import Pagination, get_page_parameter
from forms.tickets import TicketClientForm, TicketForm
import datetime
from datetime import datetime, timedelta
from io import BytesIO


@app.route('/tickets', methods=['POST', 'GET'])
def Tickets():
    if 'userid' not in session or session['userid'] == None:
        return redirect(url_for('Login'))

    else:
        admin = session['admin']

        form = TicketClientForm()
        systems = System.query.filter(System.deleted == False).all()
        system_list=[("{}".format(i.id), i.name) for i in systems]
        form.license_id.choices = system_list

        if request.method == "POST" and form.validate_on_submit():
            return redirect(url_for('OpenTicket', client=form.client.data, system=form.license_id.data))
        
        else:
            q = request.args.get('q')
            
            if q:
                search = "{}".format(q)
                tickets = Ticket.query.join("client").filter(Ticket.deleted == False).order_by(Ticket.date.desc())\
                    .filter((Client.bussiness_name.like('%' + q + '%')) | Client.cnpj.like('%' + q + '%') | \
                        (Client.cpf.like('%' + q + '%')))
            else:
                tickets = Ticket.query.join("client").filter(Ticket.deleted == False).order_by(Ticket.date.desc())

            page = request.args.get(get_page_parameter(), type=int, default=1)

            tickets_list = tickets.offset(5 * (page-1)).limit(5)

            pagination = Pagination(page=page, total=tickets.count(), search=False, record_name='tickets', per_page=5)

            if not q:
                q = ""

            message = None

            if 'message' in session and session['message'] != None:
                message = session['message']
                session['message'] = None

        return render_template('ticket/index.html', admin=admin, tickets=tickets_list, pagination=pagination, search=q, message=message, form=form)



@app.route('/ticket/<client>/<system>', methods=['POST', 'GET'])
def OpenTicket(client, system):
    if 'userid' not in session or session['userid'] == None:
        return redirect(url_for('Login'))

    else:
        admin = session['admin']

        form = TicketForm()

        license_selected = License.query.filter(License.client_id == client).filter(License.system_id == system).first()   
        services = Service.query.filter(Service.deleted == False).all()
        history = Ticket.query.join('license').filter(Ticket.client_id == license_selected.client_id)\
            .filter(License.system_id == system).order_by(Ticket.date.desc()).all()

        totalprice = 0

        warranty = False
        final_warranty = license_selected.date + timedelta(license_selected.system.warranty)

        if datetime.now() < final_warranty:
            warranty = True     
    
        form.license.data = license_selected.system.id
        form.client_id.data = license_selected.client.id

        if request.method == "POST" and form.validate_on_submit():
            new_ticket = Ticket(
                client_id = form.client_id.data, 
                license_id = license_selected.id, 
                date = datetime.now(), 
                summary = form.summary.data, 
                problem = form.problem.data, 
                status = 1, 
                responsable_tech = form.responsable_tech.data,
                contact_name = form.contact_name.data,
                resolution = form.resolution.data,
                deleted = False
            )
            db.session.add(new_ticket)
            db.session.commit()
            
            for s in form.services:
                service = Service.query.filter(Service.id == s.data).first()
                new_ticket.services.append(service)
                db.session.commit()

            for file in form.ticket_files.data:
                if file.filename: 
                    newFile = TicketFile(
                        name = file.filename, 
                        data = file.read(), 
                        ticket_id = new_ticket.id, 
                        deleted = False
                    )
                    db.session.add(newFile)
                    db.session.commit()     

            newcomment = None

            if(form.comment.data):
                newcomment = Comment(
                    ticket_id = new_ticket.id, 
                    user_id = session['userid'], 
                    date = datetime.now(),
                    comment = form.comment.data
                )         
                db.session.add(newcomment)
                db.session.commit()        

            
            for file in form.commentfile.data:
                if file.filename: 
                    
                    if not newcomment:
                        newcomment = Comment(
                            ticket_id = new_ticket.id, 
                            user_id = session['userid'], 
                            date = datetime.now(),
                        )
                        db.session.add(newcomment)
                        db.session.commit()  
                    
                    newFile = CommentFile(
                        name = file.filename, 
                        data = file.read(), 
                        comment_id = newcomment.id, 
                        deleted = False
                    )
                    db.session.add(newFile)
                    db.session.commit()   
                                   
            session['message'] = "Chamado aberto!"
            return redirect(url_for('Tickets'))

        else:            
            return render_template('ticket/ticket.html',admin=admin, totalprice=totalprice, history=history, form=form, license=license_selected, warranty=warranty, services=services)



@app.route('/ticket', methods=['POST', 'GET'])
def GetTicket():
    if 'userid' not in session or session['userid'] == None:
        return redirect(url_for('Login'))

    else:
        admin = session['admin']

        ticket_id = request.args.get('ticket')
        ticket = Ticket.query.filter(Ticket.id == ticket_id).first()
        files = ticket.files

        history = Ticket.query.join('license').filter(Ticket.client_id == ticket.client_id).filter(Ticket.id != ticket_id)\
            .filter(License.system_id == ticket.license.system_id).order_by(Ticket.date.desc()).all()

        list_serv = []
        totalprice = 0

        for s in ticket.services.all():
            list_serv.append(s.id)
            totalprice = totalprice + s.price

        form = TicketForm(obj=ticket)

        warranty = False
        final_warranty = ticket.license.date + timedelta(ticket.license.system.warranty)
        services = Service.query.filter(Service.deleted == False).all()
        comments = ticket.comments

        if datetime.now() < final_warranty:
            warranty = True     
    
        if request.method == "POST" and form.validate_on_submit():   
            ticket.summary = form.summary.data
            ticket.problem = form.problem.data
            ticket.status = form.status.data
            ticket.responsable_tech = form.responsable_tech.data         
            ticket.contact_name = form.contact_name.data
            ticket.resolution = form.resolution.data
            ticket.total_value = totalprice

            for s in ticket.services:
                if s.id not in form.services:
                    service = Service.query.filter(Service.id == s.id).first()
                    ticket.services.remove(service)
                    db.session.commit()

            for s in form.services:
                servicedb = ticket.services.filter(services == s.data).count()
                if servicedb == 0:
                    service = Service.query.filter(Service.id == s.data).first()
                    ticket.services.append(service)
                    db.session.commit()

            for file in form.ticket_files.data:
                if file.filename: 
                    newFile = TicketFile(
                        name = file.filename, 
                        data = file.read(), 
                        ticket_id = ticket.id, 
                        deleted = False
                    )
                    db.session.add(newFile)

            newcomment = None

            if(form.comment.data):
                newcomment = Comment(
                    ticket_id = ticket.id, 
                    user_id = session['userid'], 
                    date = datetime.now(),
                    comment = form.comment.data
                )         
                db.session.add(newcomment)
                db.session.commit()        

            
            for file in form.commentfile.data:
                if file.filename: 
                    
                    if newcomment == None:
                        newcomment = Comment(
                            ticket_id = ticket.id, 
                            user_id = session['userid'], 
                            date = datetime.now(),
                        )
                        db.session.add(newcomment)
                        db.session.commit()  
                    
                    newFile = CommentFile(
                        name = file.filename, 
                        data = file.read(), 
                        comment_id = newcomment.id, 
                        deleted = False
                    )
                    db.session.add(newFile)

                
            db.session.commit()                        
                                   
            session['message'] = "Alterações realizadas!"
            return redirect(url_for('Tickets'))

        else:            
            return render_template('ticket/ticket.html',admin=admin, comments=comments, history=history, form=form, totalprice=totalprice, listserv=list_serv, license=ticket.license, warranty=warranty, files=files, services=services)



@app.route('/get-licenses/<id>')
def GetLicenses(id):
    if 'userid' not in session or session['userid'] == None:
        return redirect(url_for('Login'))
    
    else:
        licenses = License.query.filter(License.deleted == False).filter(License.client_id == id).all()
        system_list=[]

        for item in licenses:
            system_list.append(item.system.id)

        return jsonify(system_list)




@app.route('/download-ticket-file/<id>')
def DownloadTicketFile(id):
    file = TicketFile.query.filter(TicketFile.id == id).first()
    return send_file(BytesIO(file.data), attachment_filename=file.name, as_attachment=True)


    
@app.route('/download-comment-file/<id>')
def DownloadCommentFile(id):
    file = CommentFile.query.filter(CommentFile.id == id).first()
    return send_file(BytesIO(file.data), attachment_filename=file.name, as_attachment=True)