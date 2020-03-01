from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email
from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[InputRequired('Preencha este campo.')])
    password = PasswordField('Senha', validators=[InputRequired('Preencha este campo.')])

