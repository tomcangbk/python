import json, requests

url = "https://bittrex.com/api/v1.1/public/getmarkets"
resp = requests.get(url=url)
data = json.loads(resp.text)
btc = []
for i in data["result"]:
	if "BTC" in i["MarketName"]:
		btc.append(i["MarketName"])
	else:
		pass
price = {}
for i in btc:
	url2 = "https://bittrex.com/api/v1.1/public/getmarketsummary?market=" + i
	resp2 = requests.get(url=url2)
	data2 = json.loads(resp2.text)
	price["i"] = data2["result"]["Last"]
print(price)
