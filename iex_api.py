
#for all of the supported symbols check out:
#https://api.iextrading.com/1.0/ref-data/symbols

#using IEX cloud API
from iexfinance.refdata import get_symbols
from iexfinance.stocks import Stock


class IEX:
	def __init__(self, user):
		self.user = user

	def get_stock(self, ticker_id):
		return Stock(ticker_id)

	def purchase_stocks(self, ticker_id, quantity):
		stock = self.get_stock(ticker_id)
		print(stock.get_price())
		cost = stock.get_price() * int(quantity) * 100
		print(cost)



