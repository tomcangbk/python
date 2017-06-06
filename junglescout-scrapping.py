# Scrapping junglescout.com to get niche product of amazon
# by the way, with this code below we can only get about <2000 records because the id of product and group id is dynamic
# I have no idea for this issue now :(

import requests
import json
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
with open('setting.json') as data_file:    
    sv = json.load(data_file)
""" setting.json
{'avr price max': '100',
 'avr price min': '0',
 'avr units solds max': '2000',
 'avr units solds min': '400',
 'limit page': 2,
 'limit weight': 1,
 'max page': 10,
 'price max': 60,
 'price min': 15,
 'rank max': 2000,
 'rank min': 400,
 'review max': 2000,
 'review min': 0} """
# Login to web with url: https://members.junglescout.com/users/sign_in.json and get token
# niche_url = "https://members.junglescout.com/#/niche"

body = {"user":{"login":your-accout, "password":your-password}}  
myurl = "https://members.junglescout.com/users/sign_in.json"

req = urllib.request.Request(myurl)
req.add_header('Content-Type', 'application/json; charset=utf-8')
jsondata = json.dumps(body)
jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
req.add_header('Content-Length', len(jsondataasbytes))
response = urllib.request.urlopen(req, jsondataasbytes)
bsObj0 = BeautifulSoup(response, "lxml")
dict1 = bsObj0.find("p").get_text()
dict1 = dict1[50:]
token = dict1[:32]
print(token)

# Request to get content of page include the product group id
getid_url = "http://members.junglescout.com/api/v1/keywords/get_keywords?query=towel&direction=desc&column=opportunity_score&per_page=200&page=2&initialPageLoad=false&averagePriceMin=0&averagePriceMax=100&competitionMin=0&competitionMax=100&demandMin=0&demandMax=1000&listingQualityScoreMin=0&listingQualityScoreMax=100&opportunityScoreMin=0&opportunityScoreMax=100&wordCountMin=1&wordCountMax=4&country=us&categories=%5B%22Baby%22%5D"
req2 = urllib.request.Request(getid_url)
req2.add_header('token', token)
req2.add_header('Content-Type', 'application/json; charset=utf-8')
req2.add_header('Host', 'members.junglescout.com')
req2.add_header('Connection', 'keep-alive')

response2 = urllib.request.urlopen(req2)
# print(response2.headers)
bsObj = BeautifulSoup(response2, "lxml")
print(bsObj)
# Parse bsObj to get group product id
p_tag = bsObj.find("p").get_text()
d = json.loads(p_tag)
e = d["data"]
g = e["keywords"]
list_id = []
for item in g:
    id_ = item["id"]
    list_id.append(id_)
list_id

"""
It will response a id list like this
[44559098,
 44518201,
 39413267,
 39413369,
 39413425,
 44505012,
 ...
 44573980,
 48741489,
 49657530]
 """
 # Request to get product
get_prd = "http://members.junglescout.com/api/v1/keywords/keyword_data?id=44505012" #+ str(id_)
req3 = urllib.request.Request(get_prd)
req3.add_header('token', token)
req3.add_header('Content-Type', 'application/json; charset=utf-8')
req3.add_header('Host', 'members.junglescout.com')
req3.add_header('Connection', 'keep-alive')

response3 = urllib.request.urlopen(req3)
# print(response2.headers)
bsObj2 = BeautifulSoup(response3, "lxml")

# Parse json to get product detail : each column is a list
p_tag2 = bsObj2.find("p").get_text()
d2 = json.loads(p_tag2)
e2 = d2["data"]
g2 = e2["products"]

# Create list-column of variables
list_product_name = []
list_product_link = []
list_product_review = []
list_product_price = []
list_product_rank = []
list_product_estsale = []
list_product_revenue = []

g2[0]
"""
{'all_fees': {'fulfillment_fee': 2.99,
  'referral_fee': 1.95,
  'total_fee': 4.94,
  'variable_closing_fee': 0.0},
 'amz_store_code': 'us',
 'amz_store_id': None,
 'asin': 'B01I5MPR1G',
 'brand': 'Mukin',
 'bsr_product': True,
 'calc_category': 'Baby',
 'calc_estimated_revenue': 11691.0,
 'calc_net': '8.02',
 'category': 'Baby',
 'country': None,
 'created_at': '2016-08-25T13:45:32.943Z',
 'fba_fee': '4.97',
 'height': 1.5,
 'id': 47921767,
 'image_url': 'https://images-na.ssl-images-amazon.com/images/I/51NJdg8EFLL._SL75_.jpg',
 'index_elasticsearch': True,
 'last_indexed_at': '2017-05-08T12:56:37.832Z',
 'last_scraped': 'May 6, 2017',
 'length': 8.3,
 'listing_quality_score': 65.0,
 'number_sellers': 3,
 'parent_asin': None,
 'pd_est_sales': 900,
 'pd_price': '12.99',
 'pd_rank': 1287,
 'price': 12.99,
 'product_name': 'Baby Muslin Washcloths and Towels - Natural Organic Cotton Baby Wipes - Soft Newborn Baby Face Towel and Muslin Washcloth for Sensitive Skin- Baby Registry as Shower Gift, 5 Pack 10x10 inches By Mukin',
 'product_tier': 'Standard (Large)',
 'product_url': 'http://www.amazon.com/dp/B01I5MPR1G',
 'rating': 4.4,
 'review_datum': {'rating': 4.4, 'reviews': 25},
 'reviews': 25,
 'seller': 'Mukin',
 'seller_type': 'FBA',
 'state': 'active',
 'unavailable': False,
 'updated_at': '2017-05-08T12:56:12.129Z',
 'variants': False,
 'weight': 0.25,
 'width': 5.6}
 """
 import pandas as pd
df_prd = pd.DataFrame(columns=('1.Product Name', '2.Product Link', '3.Review', '4.Price', '5.Rank', '6.EST Sales', '7.Revenue') )
for item in g2:
    item_detail = {"1.Product Name": item["product_name"],
                           "2.Product Link": item["product_url"],
                           "3.Review": item["reviews"],
                           "4.Price": item["price"],
                           "5.Rank": item["pd_rank"],
                           "6.Weight": item["weight"],
                           "7.EST Sales": item["pd_est_sales"],
                           "8.Revenue": item["calc_estimated_revenue"]}
    df_prd = df_prd.append(item_detail, ignore_index=True)
df_prd # The result is df_prd
