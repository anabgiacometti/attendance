from app import app, db, mail
from flask import render_template, redirect, url_for, request, abort, session
from models.user import User
from forms.login import LoginForm
from views.dashboard import Home
from flask_mail import Message
import random, string

@app.route('/', methods=["GET", "POST"])
def Login():
    form = LoginForm()
    message = None

    if 'message' in session:
        message = session['message']
        session['message'] = None

    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if not user:
            form.username.errors.append('Usuário não encontrado.')
        
        elif form.password.data != user.password:
            form.password.errors.append('Senha incorreta.')

        elif user.active == False:
            form.username.errors.append('Usuário inativo.')

        else:
            session['username'] = user.username
            session['userid'] = user.id
            session['admin'] = user.admin
            return redirect(url_for('Home'))

    return render_template('login/index.html', form=form, message_pass=message, login=True)

@app.route('/logout')
def Logout():
    session.clear()
    return redirect(url_for('Login'))


def randomString(stringLength=4):
    letters = string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))


def sendMail(name, username, senha, email):
    msg = Message("Attendance: Recuperação de Senha", recipients=[email])
    msg.html = render_template('email/recoverpassword.html', name = name, username = username, senha = senha)
    mail.send(msg)


@app.route('/recoverpass/<username>')
def RecoverPass(username):
    random = randomString()
    user = User.query.filter(User.username == username).first()
    
    if not user:
        session['message'] = "Username não encontrado."

    else:
        user.password = "{}{}".format(user.username, random)
        db.session.commit()
        sendMail(user.name, user.username, user.password, user.email)
        session['message'] = "Uma nova senha foi encaminhada à seu e-mail."

    return redirect(url_for('Login'))
