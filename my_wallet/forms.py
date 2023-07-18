from flask_wtf import FlaskForm
from wtforms import DateField, StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import datetime,date


def date_today(form, field):
    if field.data > date.today():
        raise ValidationError("Must be lower than today")

class MovementForm(FlaskForm):
    currency_in = SelectField("Moneda", validators=[DataRequired("currency obligatorios")], choices=[("EUR", "Euros")])
    quantity_in = FloatField("Cantidad", validators=[DataRequired("Cantidad obligatoria")])
    currency_out = SelectField("Currency", validators=[DataRequired("Moneda obligatoria")], choices=[("BTC", "BitCoins")])
    quantity_out = FloatField("Cantidad", validators=[DataRequired("Cantidad obligatoria")])
    submit = SubmitField("Enviar")