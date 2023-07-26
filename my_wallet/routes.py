import requests
from my_wallet import app
from my_wallet.forms import MovementForm
from flask import render_template, request, redirect, flash, session
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
    #rate = ""
    fecha = datetime.datetime.now()
    precio_u = session.get('precio_u', 0.0)
    

    form = MovementForm()

    if request.method == "GET":
        return render_template("purchase.html", the_form=form, date_now=fecha, p_u=precio_u)
    elif request.method == "POST" and form.validate_on_submit():
        try:
            if 'calculate' in request.form:  # Botón "Calcular" presionado
                # Realizar la llamada a la API
                currency_from = form.currency_in.data
                currency_to = form.currency_out.data
                if currency_from == currency_to:
                    flash("Error: Both Currencies Cant Be The Same.")
                    return render_template("purchase.html", the_form=form, date_now=fecha, p_u=precio_u)

                url = f'https://rest.coinapi.io/v1/exchangerate/{currency_from}/{currency_to}?apikey={app.config.get("API_KEY")}'
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    rate = data.get('rate')

                    # Actualizar la variable de sesión
                    session['precio_u'] = float(rate)

                    # Calcular la cantidad de moneda de destino
                    quantity_in = float(form.quantity_in.data)
                    quantity_out = quantity_in * float(rate)

                    session['currency_from'] = currency_from
                    session['currency_to'] = currency_to

                    return render_template("purchase.html", the_form=form, date_now=fecha, p_u=precio_u, quantity=quantity_out)

                else:
                    flash(f"Error al obtener la tasa de cambio: {response.status_code}")
                    return render_template("purchase.html", the_form=form, date_now=fecha, p_u=precio_u)
            


            elif "comprar" in request.form:  # Boton "Comprar" presionado
                # Obtener los datos del formulario
                fecha = datetime.datetime.now()
                currency_from = form.currency_in.data
                currency_to = form.currency_out.data
                quantity_in = float(form.quantity_in.data)
                precio_u = float(session.get("precio_u", 0.0))
                quantity_out = precio_u * quantity_in
                alm_currency_from = session.get('currency_from')
                alm_currency_to = session.get('currency_to')

                # Verificar si se modificaron Datos
                if currency_from != alm_currency_from or currency_to != alm_currency_to:
                    
                    flash(f'no puedes cambiar monedas')
                    return render_template("purchase.html", the_form=form, date_now=fecha, p_u=precio_u)
                else:
                    # Insertar los datos en la base 
                    dao.insert(Registros(fecha, currency_from, quantity_in, currency_to, quantity_out, precio_u))

                # Limpiar la variable de sesión despues de la compra
                    session.pop("precio_u", None)

                    return redirect("/")
            else:

                return render_template("purchase.html", the_form=form, date_now=fecha, p_u=precio_u)


        except requests.exceptions.RequestException as e:
                flash(f'Error de conexión: {e}')
                return render_template("purchase.html", the_form=form, date_now=fecha, p_u=precio_u)

    
@app.route("/status", methods=["GET"])
def status():
    try:
        the_stats = dao.get_all()
        return render_template("index.html", stats= the_stats, title="Status")
    except ValueError as e:
        flash("Su fichero de datos está corrupto")
        flash(str(e))
        return render_template("status.html", stats=[], title="Status")

