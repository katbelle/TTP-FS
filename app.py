#the beginnings of the IEX project
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
import json
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from pprint import pformat
from sqlalchemy.sql import func, exists

from iex_api import IEX
from model import User, connect_to_db, db

app = Flask(__name__)
app.secret_key = "Stockify"
app.jinja_env.undefined = StrictUndefined


def get_state(session):
	return {
		'loggedIn': bool(session.get('logged_in_user')),
	}


@app.route('/')
def index():
	"""Login/Landing Page"""
	#must do the following steps for each route to export var logged_in
	return render_template("sign_in.html")


@app.route("/transactions")
def get_transactions():
	"""Display history of user transactions"""
	transactions = Transaction.query.distinct(Transaction.stock_id).all()
	return render_template("transactions.html",
						   state=get_state(session))

#Build out an about me page if theres time
# @app.route('/about')
# def render_about_me():
# 	"""An about me page"""
# 	return render_template("about.html")


@app.route("/sign-up", methods=["GET", "POST"])
def register_process():
	"""Registration form and process"""
	if request.method == "GET":
		return render_template("register.html")


	email = request.form.get("email")
	password = request.form.get("password")

	if User.query.filter(User.email == email).first():
		flash('An account with that email already exists!')
		#import pdb; pdb.set_trace()
		return render_template("register.html")

	#good place to add password encryption because this
	#checks that the account doesn't already exist.
	user = User(email=email, password=password)
	db.session.add(user)
	db.session.commit()

	session["logged_in_user"] = user.user_id

	flash('Success! You made an account')
    #later when I think routes can customize line below for specific redirect
	return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
	"""Log in."""
	if request.method == "GET":
		return render_template("sign_in.html")

	else:
		email = request.form.get("email")
		password = request.form.get("password")

		q = User.query
		if q.filter((User.email == email), (User.password == password)).first():
			session["logged_in_user"] = q.filter(User.email == email).one().user_id
			flash("Logged in!")
			return redirect("/")
		else:
			flash("The e-mail or password is incorrect.")
			return render_template("sign_in.html")


@app.route("/purchase", methods=["GET","POST"])
def purchase_stock():
	""" Purchase Stock """
	if request.method == "POST":
		ticker_id = request.form.get("ticker_id")
		quantity = request.form.get("quantity")
		user = None
		iex = IEX(user)
		iex.purchase_stocks(ticker_id, quantity)


	return render_template("portfolio.html")
	


@app.route("/logout")
def logout():
	"""log out"""
	print("Log out route accessed", session.get("logged_in_user"))
	del session["logged_in_user"]
	flash("you're logged out")
	return redirect("/")



if __name__ == "__main__":

	app.debug = True
	
	app.jinja_env.auto_reload = app.debug

	connect_to_db(app)

	# Use the DebugToolbar
	DebugToolbarExtension(app)
	app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

	app.run(host='0.0.0.0')