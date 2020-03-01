from app import app, db
from flask import render_template, redirect, url_for, request, abort, session
from models.system import System
from forms.systems import SystemForm
from flask_paginate import Pagination, get_page_parameter

@app.route('/systems')
def Systems():
    if 'userid' not in session or session['userid'] == None or 'admin' not in session or session['admin'] == False or session['admin'] == None:
        return redirect(url_for('Login'))

    else:
        admin = session['admin']

        q = request.args.get('q')
        
        if q:
            search = "{}".format(q)
            systems = System.query.filter(System.deleted == False).order_by(System.name).filter(System.name.like('%' + q + '%'))
        else:
            systems = System.query.filter(System.deleted == False).order_by(System.name)

        page = request.args.get(get_page_parameter(), type=int, default=1)

        system_list = systems.offset(5 * (page-1)).limit(5)

        pagination = Pagination(page=page, total=systems.count(), search=False, record_name='systems', per_page=5)

        if not q:
            q = ""

        message = None

        if 'message' in session and session['message'] != None:
            message = session['message']
            session['message'] = None

        return render_template('system/index.html', admin=admin, systems=system_list, pagination=pagination, search=q, message=message)

@app.route('/system', methods=["GET", "POST"])
def UniqueSystem():
    if 'userid' not in session or session['userid'] == None or 'admin' not in session or session['admin'] == False or session['admin'] == None:
        return redirect(url_for('Login'))
    
    else:
        admin = session['admin']
        form = SystemForm()

        if request.method == "POST" and form.validate_on_submit():
            
            if not form.id.data:
                system_db = System.query.filter(System.deleted == False).filter(System.name == form.name.data).first()
                
                if system_db: 
                    form.name.errors.append('Sistema já cadastrado.')
                    return render_template('system/system.html',admin=admin, form=form) 

                else:
                    new_system = System(
                        name = form.name.data, 
                        warranty = form.warranty.data,
                        obs = form.obs.data, 
                        deleted = False
                    )
                    db.session.add(new_system)
                    db.session.commit()

                    session['message'] = "Sistema cadastrado!"

                    return redirect(url_for('Systems'))

            else:
                system_db = System.query.filter(System.id == form.id.data).first()
                system_duplicated = System.query.filter(System.deleted == False).filter((System.id != form.id.data) & (System.name == form.name.data)).first()
    
                if system_duplicated: 
                    form.name.errors.append('Sistema já cadastrado.')
                    return render_template('system/system.html',admin=admin, form=form) 
                    
                system_db.name = form.name.data
                system_db.warranty = form.warranty.data
                system_db.obs = form.obs.data
                
                db.session.commit()

                session['message'] = "Alterações salvas!"

                return redirect(url_for('Systems'))

        else:
            systemid = request.args.get('system')

            if systemid:        
                system = System.query.filter(System.id == systemid).first()
                form = SystemForm(obj=system)
       
        return render_template('system/system.html',admin=admin, form=form)



@app.route('/delsystem/<id>')
def DeleteSystem(id):
    if 'userid' not in session or session['userid'] == None or 'admin' not in session or session['admin'] == False or session['admin'] == None:
        return redirect(url_for('Login'))
    
    else:
        system = System.query.filter(System.id == id).first()
        system.deleted = True
        db.session.commit()

        session['message'] = "Sistema excluído!"

        return redirect(url_for('Systems'))
