from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	"""Users of IEX Web App"""
	__tablename__ = "users"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	email = db.Column(db.String(100), nullable=True)
	password = db.Column(db.String(64), nullable=True)
	cash_money = db.Column(db.Integer, default=500000, nullable=False)

# @NOTE: With more time would implement Stock model
# class Stock(db.Model):
# 	"""Different Companies that have stocks"""
# 	__tablename__ = "stocks"

# 	stock_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
# 	abbr_stock_name = db.Column(db.String(10), nullable=False)
# 	stock_price = db.Column(db.Integer,nullable=False)

class Transaction(db.Model):
	"""A given transaction for a user"""
	__tablename__ = "transactions"

	transaction_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

	cost = db.Column(db.Integer, nullable=False)
	quantity = db.Column(db.Integer, nullable=False)
	stock_price = db.Column(db.Integer, nullable=False)
	ticker_id = db.Column(db.String(255), nullable=False)
	type = db.Column(db.String(255), nullable=False)
	user = db.relationship(
		"User",
		backref=db.backref("transactions", order_by=transaction_id)
	)


def connect_to_db(app):
	"""Connect the database to the Flask app."""

	# Configure to use PstgreSQL database

	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://local:local@db:5432/stockify'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.app = app
	db.init_app(app)


if __name__ == "__main__":
	from app import app
	connect_to_db(app)
	print("Woot! Connected to DB.")