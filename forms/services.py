from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, BooleanField, HiddenField, TextAreaField, DecimalField
from wtforms.validators import InputRequired, Length
from wtforms.fields.html5 import EmailField


class ServiceForm(FlaskForm):
    id = HiddenField()
    name = StringField('Nome', validators=[InputRequired('Preencha este campo.')])
    price = StringField('Valor', validators=[InputRequired('Preencha este campo.')])
    obs = TextAreaField('Observação')

