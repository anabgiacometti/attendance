from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, BooleanField, HiddenField, TextAreaField
from wtforms.validators import InputRequired
from wtforms.fields.html5 import EmailField


class SystemForm(FlaskForm):
    id = HiddenField()
    name = StringField('Nome', validators=[InputRequired('Preencha este campo.'), ])
    warranty = IntegerField('Garantia', validators=[InputRequired('Preencha este campo.')])
    obs = TextAreaField('Observação')

