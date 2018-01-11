class Order:
	def __init__(self, api, pair, amount, offset, sell = True, fixed = True):
		self.api = api
		self.pair = pair
		self.amount = float(amount)
		self.sell = sell
		self.offset = float(offset)
		self.fixed = fixed
   		self.rate = 0
		self.getRate()
		self.price = self.rate
		self.done = 0
		
	def getRate(self):
   		pair = self.api.prices[self.pair]
		if self.sell:
			self.rate = float(pair["highestBid"])
		else:
			self.rate = float(pair["lowestAsk"])

	def updatePrice(self):
   		pair = self.api.prices[self.pair]
		if self.sell:
			self.price = float(pair["highestBid"])
		else:
			self.price = float(pair["lowestAsk"])

