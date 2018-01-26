#!/usr/bin/python

import json, requests
import gspread
import datetime
from binance.client import Client
from oauth2client.service_account import ServiceAccountCredentials

# Get date time
def get_time():
	now = str(datetime.datetime.now())[:10]
	return now
	
# Get bittrex change
def get_bittrex_change(yesterday_price, current_price):
	change = (current_price - yesterday_price)*100/yesterday_price
	return change 
	
# Get bittrex prices
def get_bittrex():

	# Get pair
	bittrex = {}
	bittrex["time"] = get_time()
	url1 = "https://bittrex.com/api/v1.1/public/getmarkets"
	resp = requests.get(url=url1)
	data = json.loads(resp.text)
	
	
	# Get pairs 
	btc_bittrex = []
	for i in data["result"]:
		if "BTC" in i["MarketName"]:
			btc_bittrex.append(i["MarketName"])
		else:
			pass
			
	# Get pairs values
	bittrex["pair"] = {}
	
	for name in btc_bittrex:
		url2 = "https://bittrex.com/api/v1.1/public/getmarketsummary?market=" + name
		resp2 = requests.get(url=url2)
		data2 = json.loads(resp2.text)
		sub_data2 = {}
		
		# Extract data from data2
		sub_data2["name"] 		= name
		sub_data2["last_price"] = data2["result"][0]["Last"]
		sub_data2["volume"] 	= data2["result"][0]["Volume"]
		sub_data2["change"] 	= get_bittrex_change(data2["result"][0]["PrevDay"], data2["result"][0]["Last"])
		# print(sub_data2)
		bittrex["pair"][name]  = sub_data2

	return bittrex
# bittrex = get_bittrex()

# Get binance prices
def get_binance():

    binance         = {}
    binance["time"] = get_time()
    binance["pair"] = {}
    #sub_data2      = {}
    url             = "https://www.binance.com/api/v1/ticker/24hr"
    resp            = requests.get(url=url)
    data            = json.loads(resp.text)

    # Get pairs
    btc_binance = []
    for item in data:
        if "BTC" in item["symbol"]:
		
			      # Extract data
            sub_data2       = {}
            sub_data2["name"]       = item["symbol"]
            sub_data2["last_price"] = float(item["lastPrice"])
            sub_data2["volume"]     = float(item["volume"])
            sub_data2["change"]     = float(item["priceChangePercent"])
            # print item["symbol"]
            binance["pair"][item["symbol"]] = sub_data2
        else:
            pass
    return binance
# binance = get_binance()
