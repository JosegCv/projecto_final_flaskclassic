from my_wallet import app
from my_wallet.forms import *
from flask import render_template, request, redirect, flash, url_for


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/purchase")
def purchase():
    return render_template("purchase.html")

@app.route("/status")
def status():
    return render_template("status.html")
