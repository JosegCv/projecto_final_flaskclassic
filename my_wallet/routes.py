import requests
from my_wallet import app
from my_wallet.forms import MovementForm
from flask import render_template, request, redirect, flash
from my_wallet.models import MovementDAOsqlite, CURRENCIES, Registros
import sqlite3
import datetime
dao = MovementDAOsqlite(app.config.get("PATH_SQLITE"))


@app.route("/")
def index():
    
    try:
        the_movs = dao.get_all()
        return render_template("index.html", movs=the_movs, title="Inicio")
    except ValueError as e:
        flash("Su fichero de datos está corrupto")
        flash(str(e))
        return render_template("index.html", movs=[], title="Inicio")
    

@app.route("/purchase", methods=["GET","POST"])
def Purchase():
    fecha = datetime.datetime.now()
    precio_u = ""
    

    form = MovementForm()

    if request.method == "GET":
        return render_template("purchase.html", the_form=form, date_now=fecha, p_u=precio_u)
    elif request.method == "POST":
        try:
            # Realizar la llamada a la API 
            currency_from = form.currency_in.data
            currency_to = form.currency_out.data
            url = f'https://rest.coinapi.io/v1/exchangerate/{currency_from}/{currency_to}?apikey={app.config.get("API_KEY")}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                rate = data.get('rate')
                flash(f'Tasa de cambio actualizada: 1 {currency_from} = {rate} {currency_to}')

                # Calcular la cantidad de moneda de destino
                precio_u = "{:.5f}".format(float(rate))
                quantity_in = form.quantity_in.data
                quantity_out = float(quantity_in) * float(rate)
                form.quantity_out.data = "{:.5f}".format(quantity_out)  # Formatear a 5 decimales

                dao.insert(Registros(fecha, currency_from, form.quantity_in.data,
                                    currency_to, form.quantity_out.data, precio_u))
                return redirect("/")
            else:
                flash(f'Error al obtener la tasa de cambio: {response.status_code}')
                return render_template("purchase.html", the_form=form)
        except requests.exceptions.RequestException as e:
            flash(f'Error de conexión: {e}')
            return render_template("purchase.html", the_form=form)

@app.route("/status", methods=["GET"])
def status():
    return render_template("status.html")

