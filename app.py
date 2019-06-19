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


def get_user(session):
	return User.query.get(session['logged_in_user'])


@app.route('/')
def index():
	"""Login/Landing Page"""
	return render_template("sign_in.html")


#Build out an about me page if theres time
# @app.route('/about')
# def render_about_me():
# 	"""An about me page"""
# 	return render_template("about.html")


@app.route("/sign-up", methods=["GET", "POST"])
def register_process():
	"""Registration form and process."""
	if request.method == "GET":
		return render_template("register.html")

	email = request.form.get("email")
	password = request.form.get("password")

	if User.query.filter(User.email == email).first():
		flash('An account with that email already exists!')
		return render_template("register.html")

	#checks that the account doesn't already exist.
	user = User(email=email, password=password)
	db.session.add(user)
	db.session.commit()

	session["logged_in_user"] = user.user_id

	flash('Success! You made an account')
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
			flash("The e-mail or password entered was incorrect.")
			return render_template("sign_in.html")


@app.route("/purchase", methods=["GET", "POST"])
def purchase_stock():
	"""Purchase Stock."""
	if not session.get("logged_in_user"):
		flash("You must be logged in to access your Portfolio")
		return redirect("/")

	user = get_user(session)

	if request.method == "POST":
		ticker_id = request.form.get("ticker_id")
		quantity = request.form.get("quantity")
		iex = IEX(user)
		success, transaction = iex.purchase_stocks(ticker_id, quantity)
		if not success:
			flash(transaction)
		else:
			flash('purchase successful')

	# @TODO: Get portfolio data from transactions to display on page.
	portfolio = iex.get_portfolio()
	total_portfolio_cost = sum(
		[stock['cost'] for stock in portfolio.values()]
	)
	return render_template("portfolio.html", portfolio=portfolio,
						   total_portfolio_cost=total_portfolio_cost,
						   user_cash_money=user.cash_money)


@app.route("/transactions", methods=["GET"])
def transactions():
	"""Display history of user transactions"""
	if not session.get("logged_in_user"):
		flash("You must be logged in to access your Portfolio")
		return redirect("/")

	user = get_user(session)
	transactions = Transaction.query.filter(user=user).all()
	return render_template("transactions.html",
						   state=get_state(session),
						   transactions=transactions)


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