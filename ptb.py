#!/usr/bin/python
# Copyright (c) 2018 Ali Raheem

import urllib2
from json import loads
from tradingApi import polo
from order import Order

def checkOrder(order):
	if order.sell:
		if(order.fixed):
			thres = order.rate - order.offset
		else:
			thres = round(order.rate - order.rate * order.offset/100, 8)
		if order.price > order.rate:
			order.rate = order.price
			print("{}: New peak rate: {}".format(order.pair, order.price))
		elif (order.price < thres):
			order.done = True
			order.api.sell(order.pair, order.amount, order.price)
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
			order.api.buy(order.pair, order.amount, order.price)
			print("buy {} on {} at {}.".format(order.amount, order.pair, order.price))
		print("{} is at {g} will order at {g}".format(order.pair, order.price, thres))


if "__main__" == __name__:
	print("Copyright (c) 2018 Ali Raheem")
	print("Poloniex Trailing Bot")
	config = loads(open('config.json', 'r').read())
	api = polo(config["api-key"], config["api-secret"])
	api.getPrices()
	orders = []
	order = Order(api, "BTC_DOGE", 100, 2.5, sell = True, fixed = False) # Sell 100 DOGE if price falls 5%
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

