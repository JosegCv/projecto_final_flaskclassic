import requests
import datetime
from flask import render_template, request, redirect, flash, session, url_for
from my_wallet import app
from my_wallet.forms import MovementForm
from my_wallet.models import MovementDAOsqlite, CURRENCIES, Registros
import time
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
    
@app.route("/purchase", methods=["GET", "POST"])
def Purchase():
    fecha = datetime.datetime.now().strftime("%H:%M")
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
                    flash("Error: Las Monedas No Pueden Ser Iguales")
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
                elif response.status_code == 400:
                    flash('Error en la peticion')
                elif response.status_code == 401:
                    flash('Error :Verifique La Clave apikey')
                elif response.status_code == 403:
                    flash('error: apikey no privileges')
                elif response.status_code == 429:
                    flash('error : Se a Alcanzado El limite De Peticions a la api')
                elif response.status_code == 550:
                    flash('error: no se encontraron datos')
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
                session['quantity_in'] = quantity_in
                alm_quantity_in = session.get('quantity_in')

                # Verificar si se modificaron Datos
                if currency_from != alm_currency_from or currency_to != alm_currency_to or quantity_in != alm_quantity_in:
                    flash(f'No esta Permitida Esta Accion Intentelo De Nuevo')
                    return render_template("purchase.html", the_form=form, date_now=fecha, p_u=precio_u)
                else:
                    # Validar que la cantidad de monedas a comprar sea positiva
                    if quantity_out <= 0:
                        flash(f'La cantidad a comprar debe ser un número positivo')
                        return render_template("purchase.html", the_form=form, date_now=fecha, p_u=precio_u)

                    # Validar que haya suficientes monedas disponibles para la compra
                    if currency_from != "EUR":
                        cantidad_actual = dao.consulta().get(currency_from, {}).get("quantity_to", 0.0)
                        cantidad_compra = dao.consulta().get(currency_from, {}).get("quantity_from", 0.0)
                        se_puede = cantidad_actual - cantidad_compra

                        if se_puede <= quantity_in:
                            flash(f'No tienes suficientes monedas para realizar esta compra')
                            return render_template("purchase.html", the_form=form, date_now=fecha, p_u=precio_u, act=cantidad_actual)

                    # Insertar los datos en la base
                    dao.insert(Registros(fecha, currency_from, quantity_in, currency_to, quantity_out, precio_u))
                        # Limpiar la variable de sesión después de la compra
                    session.pop("precio_u", None)
                    session.pop("currency_from", None)
                    session.pop("currency_to", None)

                    return redirect("/")
            else:
                return render_template("purchase.html", the_form=form, date_now=fecha, p_u=precio_u)

        except requests.exceptions.RequestException as e:
            flash(f'Error de conexión: {e}')
            return render_template("purchase.html", the_form=form, date_now=fecha, p_u=precio_u)

    else:
        flash(f'Use a Valid positive Number')
        return render_template("purchase.html", the_form=form, date_now=fecha, p_u=precio_u)


@app.route("/status", methods=["GET"])
def status():
    try:
        base = "EUR"
        the_stats = dao.consulta()  # consulta a la BD
        total_inversion = 0.0  
        total_inversion_euro = 0.0
        processed_stats = {}  # Recolectar los datos procesados en un diccionario

        # Obtener los tipos de cambio respecto al Euro (EUR) desde la API
        url = f'https://rest.coinapi.io/v1/exchangerate/{base}?apikey={app.config.get("API_KEY")}'
        response = requests.get(url)


        if response.status_code == 200:
            rates_eur = response.json()

            # Realizar cálculos con los datos del diccionario the_stats
            for currency, data in the_stats.items():
                exchange_rate = None
                for rate_info in rates_eur["rates"]:
                    if rate_info["asset_id_quote"] == currency:
                        exchange_rate = rate_info["rate"]
                        break
                quantity_to = data["quantity_to"]
                quantity_from = data["quantity_from"]
                cantidad_final = quantity_to - quantity_from

                if exchange_rate is not None:
                    cantidad_multiplicada = cantidad_final / exchange_rate

                    processed_data = {
                        "currency": currency,
                        "valor_actual": cantidad_final,
                        "exchange_rate": exchange_rate,
                        "cantidad_multiplicada": cantidad_multiplicada
                    }
                    processed_stats[currency] = processed_data

            total_inversion = 0.0
            for currency_data in processed_stats.values():
                total_inversion += currency_data["cantidad_multiplicada"]

            if "EUR" in the_stats and "quantity_to" in the_stats["EUR"] and "quantity_from" in the_stats["EUR"]:
                total_inversion_euro = total_inversion - the_stats["EUR"]["quantity_from"]
            else:
                total_inversion_euro = 0.0

        elif response.status_code == 400:
            flash('Error en la petición')
        elif response.status_code == 401:
            flash('Error: Verifique La Clave apikey')
        elif response.status_code == 403:
            flash('Error: apikey no tiene privilegios')
        elif response.status_code == 429:
            flash('Error: Se ha alcanzado el límite de peticiones a la API')
        elif response.status_code == 550:
            flash('Error: no se encontraron datos')
        else:
            flash(f"Error al obtener la tasa de cambio: {response.status_code}")

        return render_template("status.html", stats=processed_stats, original_stats=the_stats, title="Status", total_inversion=total_inversion, total_inversion_euro=total_inversion_euro)

    except ValueError as e:
        flash("Su fichero de datos está corrupto")
        flash(str(e))

    return render_template("status.html", stats={}, title="Status")