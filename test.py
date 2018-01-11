from tradingApi import polo

if "__main__" == __name__:
	api = polo("BY87ZTXL-GVSFZGS8-RONGZ7VJ-IN27ADGC", "f28c09ed1369aa6d27fb6db2371f9d79d9779583ada27ae23a1240305d42aef7233a2a395a28b75bcf370700d8bda962246857834d8c8e69a7c9e7e2f56b888b")
	print(api.getBalances()["DOGE"])
