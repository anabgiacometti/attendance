from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, BooleanField, HiddenField
from wtforms.validators import InputRequired, Email
from wtforms.fields.html5 import EmailField


class UserForm(FlaskForm):
    id = HiddenField()
    name = StringField('Nome', validators=[InputRequired('Preencha este campo.')])
    username = StringField('Nome de usuário', validators=[InputRequired('Preencha este campo.')])
    email = EmailField('E-mail', validators=[InputRequired('Preencha este campo.'), Email('E-mail inválido.')])
    admin = BooleanField('Administrador')
    active = BooleanField('Usuário ativo')

