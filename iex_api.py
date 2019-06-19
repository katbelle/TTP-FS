
#for all of the supported symbols check out:
#https://api.iextrading.com/1.0/ref-data/symbols

#using IEX cloud API
from iexfinance.stocks import Stock

from model import db, Transaction

class IEX:
	def __init__(self, user):
		self.user = user

	def get_stock(self, ticker_id):
		return Stock(ticker_id)

	def purchase_stocks(self, ticker_id, quantity):
		"""Purchase stocks and return a transaction."""
		stock = self.get_stock(ticker_id)
		price = stock.get_price() * 100
		print(price)
		cost = price * int(quantity)
		print(cost)
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
		return transaction



