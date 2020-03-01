from views.client import *
from app import app, db
from flask import render_template, redirect, url_for, request, abort, session
from models.client import Client
from forms.clients import ClientForm
from flask_paginate import Pagination, get_page_parameter

@app.route('/clients')
def Clients():
    if 'userid' not in session or session['userid'] == None:
        return redirect(url_for('Login'))

    else:
        admin = session['admin']

        q = request.args.get('q')
        
        if q:
            search = "{}".format(q)
            clients = Client.query.order_by(Client.bussiness_name).filter(Client.deleted == False).filter((Client.bussiness_name.like('%' + q + '%')) | (Client.cnpj.like('%' + q + '%')) | (Client.cpf.like('%' + q + '%')))
        else:
            clients = Client.query.order_by(Client.bussiness_name).filter(Client.deleted == False)

        page = request.args.get(get_page_parameter(), type=int, default=1)

        client_list = clients.offset(5 * (page-1)).limit(5)

        pagination = Pagination(page=page, total=clients.count(), search=False, record_name='clients', per_page=5)

        if not q:
            q = ""

        message = None

        if 'message' in session and session['message'] != None:
            message = session['message']
            session['message'] = None

        return render_template('client/index.html', admin=admin, clients=client_list, pagination=pagination, search=q, message=message)

@app.route('/client', methods=["GET", "POST"])
def UniqueClient():
    if 'userid' not in session or session['userid'] == None:
        return redirect(url_for('Login'))
    
    else:
        admin = session['admin']
        form = ClientForm()

        if request.method == "POST" and form.validate_on_submit():
    
            if not form.id.data:
                cnpj_db = Client.query.filter(Client.deleted == False).filter(Client.type == '1').filter(Client.cnpj == form.identifier.data).first()
                cpf_db = Client.query.filter(Client.deleted == False).filter(Client.type == '2').filter(Client.cpf == form.identifier.data).first()
                
                if cnpj_db or cpf_db: 
                    form.identifier.errors.append('Cliente já cadastrado.')
                    return render_template('client/client.html',admin=admin, form=form) 

                else:
                    new_client = Client()

                    new_client.type = form.type.data
                    new_client.bussiness_name = form.bussiness_name.data
                    new_client.company_name = form.company_name.data
                    new_client.zip_code = form.zip_code.data
                    new_client.state = form.state.data
                    new_client.city = form.city.data
                    new_client.district = form.district.data
                    new_client.address = form.address.data
                    new_client.number = form.number.data
                    new_client.addicional_info = form.addicional_info.data
                    new_client.contact = form.contact.data
                    new_client.phone = form.phone.data
                    new_client.email = form.email.data
                    new_client.phone_2 = form.phone_2.data
                    new_client.obs = form.obs.data
                    new_client.deleted = False

                    if form.type.data == '1':                        
                        new_client.cnpj = form.identifier.data
                        new_client.state_number = form.state_number.data
                    
                    else: 
                        new_client.cpf = form.identifier.data
                        
                    db.session.add(new_client)
                    db.session.commit()

                    session['message'] = "Cliente cadastrado!"

                    return redirect(url_for('Clients'))

            else:
                client_db = Client.query.filter(Client.id == form.id.data).first()
                cnpj_db = Client.query.filter(Client.deleted == False).filter(Client.id != form.id.data).filter(Client.type == '1').filter(Client.cnpj == form.identifier.data).first()
                cpf_db = Client.query.filter(Client.deleted == False).filter(Client.id != form.id.data).filter(Client.type == '2').filter(Client.cpf == form.identifier.data).first()
                   
                if cnpj_db or cpf_db: 
                    form.identifier.errors.append('Cliente já cadastrado.')
                    return render_template('client/client.html',admin=admin, form=form) 
                    
                client_db.type = form.type.data               

                if form.type.data == '1':                        
                    client_db.cpf = None
                    client_db.cnpj = form.identifier.data
                
                else: 
                    client_db.cpf = form.identifier.data
                    client_db.cnpj = None            

                client_db.bussiness_name = form.bussiness_name.data
                client_db.company_name = form.company_name.data
                client_db.state_number = form.state_number.data
                client_db.zip_code = form.zip_code.data
                client_db.state = form.state.data
                client_db.city = form.city.data
                client_db.district = form.district.data
                client_db.address = form.address.data
                client_db.number = form.number.data
                client_db.addicional_info = form.addicional_info.data
                client_db.contact = form.contact.data
                client_db.phone = form.phone.data
                client_db.email = form.email.data
                client_db.phone_2 = form.phone_2.data
                client_db.obs = form.obs.data

                db.session.commit()

                session['message'] = "Alterações salvas!"

                return redirect(url_for('Clients'))

        else:
            clientid = request.args.get('client')

            if clientid:        
                client = Client.query.filter(Client.id == clientid).first()
                form = ClientForm(obj=client)
                form.identifier.data = client.cnpj if client.type == 1 else client.cpf
       
        return render_template('client/client.html',admin=admin, form=form)


@app.route('/delclient/<id>')
def DeleteClient(id):
    if 'userid' not in session or session['userid'] == None:
        return redirect(url_for('Login'))
    
    else:
        client = Client.query.filter(Client.id == id).first()
        client.deleted = True
        db.session.commit()

        session['message'] = "Cliente excluído!"

        return redirect(url_for('Clients'))
