from tradingApi import polo
from json import loads

if "__main__" == __name__:
	config = loads(open('config.json', 'r').read())
	api = polo(config["api-key"], config["api-secret"])
	print(api.getBalances()["DOGE"])
