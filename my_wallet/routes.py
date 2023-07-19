from my_wallet import app
from my_wallet.forms import date_today, MovementForm
from flask import render_template, request, redirect, flash, url_for
from my_wallet.models import MovementDAOsqlite, CURRENCIES, Registros


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
    form=MovementForm()
    if request.method == "GET":
        return render_template("purchase.html", the_form = form)
    else:
        if form.validate():
            try:
                dao.insert(Registros(str(form.currency_in.data),form.quantity_in.data,
                form.currency_out.data,form.quantity_out.data))
            except ValueError as e:
                flash(str(e))
                return render_template("purchase.html", the_form = form)


@app.route("/status", methods= ["GET"])
def status():
    return render_template("status.html")
