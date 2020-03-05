from app import app, db, mail
from flask import render_template, redirect, url_for, request, abort, session
from models.user import User
from forms.users import UserForm
from flask_paginate import Pagination, get_page_parameter
from flask_mail import Message
import random
import string


def randomString(stringLength=4):
    letters = string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))


def sendMail(name, username, senha, email):
    msg = Message("Attendance: Senha de Acesso", recipients=[email])
    msg.html = render_template('email/password.html', name = name, username = username, senha = senha)
    mail.send(msg)

@app.route('/users')
def Users():
    if 'userid' not in session or session['userid'] == None or 'admin' not in session or session['admin'] == False or session['admin'] == None or 'client' not in session or session['client'] != None:
        return redirect(url_for('Login'))

    else:
        admin = session['admin']

        q = request.args.get('q')
        
        if q:
            search = "{}".format(q)
            users = User.query.order_by(User.name).filter(User.deleted == False).filter((User.username.like('%' + q + '%')) | (User.name.like('%' + q + '%')))
        else:
            users = User.query.order_by(User.name).filter(User.deleted == False)

        page = request.args.get(get_page_parameter(), type=int, default=1)

        user_list = users.offset(5 * (page-1)).limit(5)

        pagination = Pagination(page=page, total=users.count(), search=False, record_name='users', per_page=5)

        if not q:
            q = ""

        message = None

        if 'message' in session and session['message'] != None:
            message = session['message']
            session['message'] = None

        return render_template('user/index.html', admin=admin, users=user_list, pagination=pagination, search=q, message=message)

@app.route('/user', methods=["GET", "POST"])
def UniqueUser():
    if 'userid' not in session or session['userid'] == None or 'admin' not in session or session['admin'] == False or session['admin'] == None or 'client' not in session or session['client'] != None:
        return redirect(url_for('Login'))
    
    else:
        admin = session['admin']
        form = UserForm()

        if request.method == "POST" and form.validate_on_submit():
            
            if not form.id.data:
                username_db = User.query.filter(User.deleted == False).filter(User.username == form.username.data).first()
                email_db = User.query.filter(User.deleted == False).filter(User.email == form.email.data).first()
                
                if username_db or email_db:

                    if username_db: 
                        form.username.errors.append('Username já cadastrado.')

                    if email_db: 
                        form.email.errors.append('E-mail já cadastrado.')
                
                    return render_template('user/user.html',admin=admin, form=form) 

                else:
                    random = randomString()

                    new_user = User(
                        name = form.name.data, 
                        username = form.username.data, 
                        email = form.email.data, 
                        active = form.active.data, 
                        admin = form.admin.data,
                        password = "{}{}".format(form.username.data, random),
                        deleted = False
                    )
                    db.session.add(new_user)
                    db.session.commit()

                    sendMail(new_user.name, new_user.username, new_user.password, new_user.email)

                    session['message'] = "Usuário cadastrado!"

                    return redirect(url_for('Users'))

            else:
                user_db = User.query.filter(User.deleted == False).filter(User.id == form.id.data).first()
                email_db = User.query.filter(User.deleted == False).filter((User.id != form.id.data) & (User.email == form.email.data)).first()
                username_db = User.query.filter(User.deleted == False).filter((User.id != form.id.data) & (User.username == form.username.data)).first()

                if username_db or email_db:
    
                    if username_db: 
                        form.username.errors.append('Username já cadastrado.')

                    if email_db: 
                        form.email.errors.append('E-mail já cadastrado.')
                
                    return render_template('user/user.html',admin=admin, form=form) 
                    
                user_db.name = form.name.data
                user_db.active = form.active.data
                user_db.admin = form.admin.data
                user_db.email = form.email.data
                user_db.username = form.username.data

                db.session.commit()

                session['message'] = "Alterações salvas!"

                return redirect(url_for('Users'))

        else:
            userid = request.args.get('user')

            if userid:        
                user = User.query.filter(User.id == userid).first()
                form = UserForm(obj=user)
       
        return render_template('user/user.html',admin=admin, form=form)




@app.route('/deluser/<id>')
def DeleteUser(id):
    if 'userid' not in session or session['userid'] == None or 'admin' not in session or session['admin'] == False or session['admin'] == None or 'client' not in session or session['client'] != None:
        return redirect(url_for('Login'))
    
    else:
        user = User.query.filter(User.id == id).first()
        user.deleted = True
        db.session.commit()

        session['message'] = "Usuário excluído!"

        return redirect(url_for('Users'))
