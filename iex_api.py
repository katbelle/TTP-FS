from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import IEXSymbolError

from model import db, Transaction

class IEX:
	def __init__(self, user):
		self.user = user

	def get_stock(self, ticker_id):
		stock = Stock(ticker_id)
		return stock

	def purchase_stocks(self, ticker_id, quantity):
		"""Purchase stocks and return a transaction."""
		stock = self.get_stock(ticker_id)
		price = stock.get_price() * 100
		cost = price * int(quantity)

		if self.user.cash_money - cost < 0:
			return None, 'You do not have enough money.'

		self.user.cash_money = self.user.cash_money - cost
		db.session.add(self.user)

		transaction = Transaction(
			cost=cost,
			quantity=quantity,
			stock_price=price,
			ticker_id=ticker_id,
			type='buy',
			user=self.user
		)
		db.session.add(transaction)
		db.session.commit()
		return transaction, None

	def get_portfolio(self):
		""" Returns portfolio as nested dictionary """
		portfolio = {}
		for t in Transaction.query.filter(Transaction.user == self.user).all():
			# Initialize with empty dictionary for ticker_id.
			if t.ticker_id not in portfolio:
				portfolio[t.ticker_id] = {
					'quantity': 0,
					'cost': 0,
				}

			# Add up quantity and cost.
			portfolio[t.ticker_id]['quantity'] += t.quantity
			portfolio[t.ticker_id]['cost'] += t.cost

		return portfolio
