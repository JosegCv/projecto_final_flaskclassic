from my_wallet import app
from my_wallet.forms import MovementForm
from flask import render_template, request, redirect, flash
from my_wallet.models import MovementDAOsqlite, CURRENCIES, Registros, get_rate
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
    fecha= datetime.datetime.now()
    precio_u =""
    api_key=app.config.get("API_KEY")
    
    

    form=MovementForm()
    if request.method == "GET":
        return render_template("purchase.html", the_form = form, date_now=fecha,p_u=precio_u)
    else:
            try:
                dao.insert(Registros(fecha,form.currency_in.data,form.quantity_in.data,
                form.currency_out.data,form.quantity_out.data, precio_u))
                return redirect("/")
            except ValueError as e:
                flash(str(e))
                return render_template("purchase.html", the_form = form)


@app.route("/status", methods= ["GET"])
def status():
    return render_template("status.html")
