from flask_wtf import FlaskForm
from wtforms import DateField, StringField, FloatField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import datetime,date




def date_today(form, field):
    if field.data > date.today():
        raise ValidationError("Must be lower than today")

class MovementForm(FlaskForm):
    currency_in = SelectField("Moneda", validators=[DataRequired("currency obligatorios")], choices=[('EUR', 'EUR'), ('BTC', 'BTC'), ('ETH', 'ETH'),
                                                                                                    ('BNB', 'BNB'), ('ADA', 'ADA'), ('DOT', 'DOT'),
                                                                                                    ('XRP', 'XRP'), ('SOL', 'SOL'), ('USDT', 'USDT'),
                                                                                                    ('MATIC', 'MATIC')])

    quantity_in = FloatField("Cantidad", validators=[DataRequired("Cantidad obligatoria")])
    currency_out = SelectField("Currency", validators=[DataRequired("Moneda obligatoria")], choices=[('EUR', 'EUR'), ('BTC', 'BTC'), ('ETH', 'ETH'),
                                                                                                    ('BNB', 'BNB'), ('ADA', 'ADA'), ('DOT', 'DOT'),
                                                                                                    ('XRP', 'XRP'), ('SOL', 'SOL'), ('USDT', 'USDT'),
                                                                                                    ('MATIC', 'MATIC')])
    
    quantity_out = HiddenField()
    calculate = SubmitField("Calcular")
    comprar = SubmitField("Comprar")