from flask_wtf import FlaskForm 
from wtforms import HiddenField, StringField, SelectField, TextAreaField, FieldList, MultipleFileField
from wtforms.validators import InputRequired
from wtforms.fields.html5 import DateField


class TicketClientForm(FlaskForm):
    client = HiddenField(validators=[InputRequired('Selecione um cliente.')])
    license_id = SelectField('Sistema', validators=[InputRequired('Preencha este campo.')])
    
class TicketForm(FlaskForm):
    id = HiddenField()
    license = HiddenField()
    client_id = HiddenField()
    contact_name = StringField("Contato", validators=[InputRequired('Preencha este campo.')])
    summary = StringField("Resumo", validators=[InputRequired('Preencha este campo.')])
    problem = TextAreaField("Descrição do Problema", validators=[InputRequired('Preencha este campo.')])
    resolution = TextAreaField("Descrição da Solução")
    ticket_files = MultipleFileField()
    services = FieldList(HiddenField('service'))
    status = SelectField(
        'Status',
        choices=[("1", 'Aguardando Atendimento'), ("2", 'Aguardando Retorno'), ("3", 'Finalizado')])
    responsable_tech = StringField("Técnico Responsável")
    comment = TextAreaField("Comentário")
    commentfile = MultipleFileField()

