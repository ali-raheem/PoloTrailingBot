#!/usr/bin/python
# Copyright (c) 2018 Ali Raheem

import urllib2, json
from tradingApi import polo

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
			self.price = (self.price + float(pair["highestBid"]))/2
		else:
			self.price = (self.price + float(pair["lowestAsk"]))/2

def checkOrder(order):
	if order.sell:
		if(order.fixed):
			thres = order.rate - order.offset
		else:
			thres = order.rate - order.rate * order.offset/100
		if order.price > order.rate:
			order.rate = order.price
			print("{}: New peak rate: {}".format(order.pair, order.price))
		elif (order.price < thres):
			order.done = True
			api.sell(order.pair, order.amount, order.price)
			print("sell {} on {} at {}.".format(order.amount, order.pair, order.price))
		print("{} is at {} will order at {}".format(order.pair, order.price, thres))
	else:
		if(order.fixed):
			thres = order.rate + order.offset
		else:
			thres = order.rate + order.rate * order.offset/100
		if order.price < order.rate:
			order.rate = order.price
			print("{}: New peak rate: {}".format(order.pair, order.price))
		elif (order.price > thres):
			order.done = True
			api.buy(order.pair, order.amount, order.price)
			print("buy {} on {} at {}.".format(order.amount, order.pair, order.price))
		print("{} is at {} will order at {}".format(order.pair, order.price, thres))


if "__main__" == __name__:
	print("Copyright (c) 2018 Ali Raheem")
	print("Poloniex Trailing Bot")
	config = json.loads(open('config.json', 'r').read())
	api = polo(config["api-key"], config["api-secret"])
	api.getPrices()
	orders = []
	order = Order(api, "BTC_DOGE", 100, 5, sell = True, fixed = False)
	order.updatePrice()
	orders.append(order)
	while True:
		api.getPrices()
		for order in orders:
			order.updatePrice()
			if order.done:
				orders.remove(order)
				break
			checkOrder(order)

