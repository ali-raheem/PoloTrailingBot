# Copyright (c) 2018 Ali Raheem

import urllib2, json
import requests
import hmac
import hashlib
from itertools import count
import time

class polo:
	prices = {}
	def __init__(self, key, secret):
		self.key = key
		self.secret = secret
		self.nonce = count(int(time.time() * 1000))
		self.getPrices()
		
	def makeRequest(self, payload):
		payload['nonce'] = next(self.nonce)
		request = requests.Request('POST', 'https://poloniex.com/tradingApi',
								   data=payload, headers='')
		prepReq = request.prepare()
		reqSig = hmac.new(self.secret, prepReq.body, digestmod=hashlib.sha512)
		prepReq.headers['Sign'] = reqSig.hexdigest()
		prepReq.headers['Key'] = self.key

		response = request.Session().send(prepReq)
		response = json.loads(response.text)
		try:
			print(response["error"])
		except:
			return response

	def moveOrder(self, orderid, rate):
		payload = {}
		payload["command"] = "moveOrder"
		payload["orderNumber"] = orderid
		payload["rate"] = rate
		self.makeRequest(payload)
		
	def makeOrder(self, type, currencyPair, rate, amount):
		payload = {}
		payload["command"] = type
		payload["rate"] = rate
		payload["amount"] = amount
		payload["currencyPair"] = currencyPair
		selfmakeRequest(payload)

	def buy(self, currencyPair, rate, amount):
		self.makeOrder("buy", currencyPair, rate, amount)
	def sell(self, currencyPair, rate, amount):
		self.makeOrder("sell", currencyPair, rate, amount)

	def getPrices(self):
		try:
			reqUrl = "https://poloniex.com/public?command=returnTicker"
			response = urllib2.urlopen(reqUrl)
			self.prices = json.loads(response.read())
			print("Prices updated")
		except:
			print("Prices update failed")
				
	def getBalances(self):
		payload = {}
		payload["command"] = "returnBalances"
		return self.makeRequest(payload)

		
