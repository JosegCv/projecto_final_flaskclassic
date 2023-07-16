from flask_wtf import FlaskForm
from wtforms import DateField, StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import *

def date_today(form, field):
    if field.data > date.today():
        raise ValidationError("Must be lower than today")

class MovementForm(FlaskForm):
    date = DateField("Fecha", validators=[DataRequired("La Fecha es obligatoria"),date_today])
    abstract = StringField("Concepto", validators=[DataRequired("Concepto obligatorios"), Length(min=5)])
    amount = FloatField("Cantidad", validators=[DataRequired("Cantidad obligatoria")])
    currency = SelectField("Moneda", validators=[DataRequired("Moneda obligatoria")], choices=[("EUR", "Euros"), ])

    submit = SubmitField("Enviar")