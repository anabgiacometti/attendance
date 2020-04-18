from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, BooleanField, HiddenField, TextAreaField, SelectField
from wtforms.validators import InputRequired, NumberRange, Email
from wtforms.fields.html5 import EmailField


class ResellerForm(FlaskForm):
    id = HiddenField()
    type = SelectField(
        'Tipo',
        choices=[("1", 'Pessoa Jurídica'), ("2", 'Pessoa Fisica')])

    identifier = StringField('CPF', validators=[InputRequired('Preencha este campo.')])
    bussiness_name = StringField('Nome Fantasia', validators=[InputRequired('Preencha este campo.')])
    company_name = StringField('Razão Social', validators=[InputRequired('Preencha este campo.')])
    state_number = StringField('Inscrição Estadual')

    zip_code = StringField('CEP')
    state = StringField('Estado')
    city = StringField('Cidade')
    district = StringField('Bairro')
    address = StringField('Endereço')
    number = StringField('Número')
    addicional_info = StringField('Complemento')

    contact = StringField('Contato', validators=[InputRequired('Preencha este campo.')])
    phone = StringField('Telefone Principal', validators=[InputRequired('Preencha este campo.')])
    email = StringField('E-mail', validators=[InputRequired('Preencha este campo.'), Email('E-mail inválido.')])
    phone_2 = StringField('Telefone Secundário')
    
    obs = StringField('Observação')
