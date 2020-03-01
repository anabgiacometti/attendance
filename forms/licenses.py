from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, BooleanField, HiddenField, TextAreaField, SelectField, MultipleFileField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired


class LicenseForm(FlaskForm):
    id = HiddenField()
    system = SelectField('Sistema', validators=[InputRequired('Preencha este campo.')])
    client = HiddenField('Cliente', validators=[InputRequired('Selecione um cliente.')])
    date = DateField('Data de Aquisição', validators=[InputRequired('Preencha este campo.')])
    seller = StringField('Vendedor')
    serial_number = StringField('Número de Série')
    fabric_number = StringField('Número de Fábrica')
    instalation_tech = StringField('Responsável pela Instalação')
    training_tech = StringField('Responsável pelo Treinamento')
    training_client = StringField('Cliente(s) presente(s) no treinamento')
    attachments = MultipleFileField()
    obs = TextAreaField('Observação')
    


   