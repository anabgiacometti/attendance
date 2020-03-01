from app import app, db
from flask import render_template, redirect, url_for, request, abort, session
from models.service import Service
from forms.services import ServiceForm
from flask_paginate import Pagination, get_page_parameter

@app.route('/services')
def Services():
    if 'userid' not in session or session['userid'] == None or 'admin' not in session or session['admin'] == False or session['admin'] == None:
        return redirect(url_for('Login'))

    else:
        admin = session['admin']

        q = request.args.get('q')
        
        if q:
            search = "{}".format(q)
            services = Service.query.order_by(Service.name).filter(Service.deleted == False).filter(Service.name.like('%' + q + '%'))
        else:
            services = Service.query.order_by(Service.name).filter(Service.deleted == False)

        page = request.args.get(get_page_parameter(), type=int, default=1)

        service_list = services.offset(5 * (page-1)).limit(5)

        pagination = Pagination(page=page, total=services.count(), search=False, record_name='services', per_page=5)

        if not q:
            q = ""

        message = None

        if 'message' in session and session['message'] != None:
            message = session['message']
            session['message'] = None

        return render_template('service/index.html', admin=admin, services=service_list, pagination=pagination, search=q, message=message)

@app.route('/service', methods=["GET", "POST"])
def UniqueService():
    if 'userid' not in session or session['userid'] == None or 'admin' not in session or session['admin'] == False or session['admin'] == None:
        return redirect(url_for('Login'))
    
    else:
        admin = session['admin']
        form = ServiceForm()

        if request.method == "POST" and form.validate_on_submit():

            if not form.id.data:
                service_db = Service.query.filter(Service.deleted == False).filter(Service.deleted == False).filter(Service.name == form.name.data).first()
                
                if service_db: 
                    form.name.errors.append('Sistema já cadastrado.')
                    return render_template('service/service.html',admin=admin, form=form) 

                else:
                    new_service = Service(
                        name = form.name.data, 
                        price = float(form.price.data.replace(',','.')),
                        obs = form.obs.data,
                        deleted = False
                    )
                    db.session.add(new_service)
                    db.session.commit()

                    session['message'] = "Sistema cadastrado!"

                    return redirect(url_for('Services'))

            else:
                service_db = Service.query.filter(Service.id == form.id.data).first()
                service_duplicated = Service.filter(Service.deleted == False).query.filter((Service.id != form.id.data) & (Service.name == form.name.data)).first()
    
                if service_duplicated: 
                    form.name.errors.append('Sistema já cadastrado.')
                    return render_template('service/service.html',admin=admin, form=form) 
                    
                service_db.name = form.name.data
                service_db.price = float(form.price.data.replace(',','.')),
                service_db.obs = form.obs.data
                
                db.session.commit()

                session['message'] = "Alterações salvas!"

                return redirect(url_for('Services'))

        else:
            serviceid = request.args.get('service')

            if serviceid:        
                service = Service.query.filter(Service.id == serviceid).first()
                service.price = ("%.2f" % service.price).replace('.',',')
                form = ServiceForm(obj=service)
       
        return render_template('service/service.html',admin=admin, form=form)


@app.route('/delservice/<id>')
def DeleteService(id):
    if 'userid' not in session or session['userid'] == None or 'admin' not in session or session['admin'] == False or session['admin'] == None:
        return redirect(url_for('Login'))
    
    else:
        service = Service.query.filter(Service.id == id).first()
        service.deleted = True
        db.session.commit()

        session['message'] = "Serviço excluído!"

        return redirect(url_for('Services'))
