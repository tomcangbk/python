from binance.client import Client
client = Client("xxxxxxxxxxxx", "xxxxxxxxxxxxxxx")
prices = client.get_all_tickers()
price = {}
for i in prices:
	if "BTC" in i["symbol"]:
		price[i["symbol"]] = i["price"]
	else:
		pass
print price
