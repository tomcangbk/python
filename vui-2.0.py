#!/usr/bin/python

import os
import sys
import json, requests
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials

def get_now():
    return str(datetime.datetime.now()+ datetime.timedelta(hours=7))[:19]

def create_file(path, data):
    with open(path, 'w') as f:
        f.write(data)
        f.close()

# Write to file
def write_log(content):
    file_name = "/home/ubuntu/tools/logs/" + str(datetime.datetime.now()+ datetime.timedelta(hours=7))[:7] + "-datacoin.log"

    # File log created
    if os.path.isfile(file_name):
        with open(file_name, "a") as myfile:
            myfile.write(content + "\n")
    # File log not exist
    else:
        create_file(file_name, str(str(datetime.datetime.now())+ datetime.timedelta(hours=7))[:7] + " DATA LOG ----------------" + "\n")
        with open(file_name, "a") as myfile:
            myfile.write(content + "\n")

# Get date time
def get_time():
    now = str(datetime.datetime.now())[:10]
    return now

# Get bittrex prices
def get_bittrex():

    write_log(get_now() + " Start get bittrex data")
    # Get pair
    bittrex = {}
    bittrex["time"] = str(datetime.datetime.now()+ datetime.timedelta(hours=7))[:19]
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
        sub_data2["name"]   = name
        sub_data2["last_price"] = data2["result"][0]["Last"]
        sub_data2["volume"]     = data2["result"][0]["Volume"]

        bittrex["pair"][name]  = sub_data2
    write_log(get_now() + " Finish get bittrex data")
    return bittrex

# Get binance prices
def get_binance():
    write_log(get_now() + " Start get binance data")
    binance         = {}
    binance["time"] = str(datetime.datetime.now()+ datetime.timedelta(hours=7))[:19]
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
            sub_data2               = {}
            sub_data2["name"]       = item["symbol"]
            sub_data2["last_price"] = float(item["lastPrice"])
            sub_data2["volume"]     = float(item["volume"])

            binance["pair"][item["symbol"]] = sub_data2
        else:
            pass
    write_log(get_now() + " Finish get binance data")
    return binance

# Auth
def gs_auth(spreadsheet_name):
    email            = "tomcangbk@gmail.com"
    key              = "client_secret.json"

    scope               = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(key, scope)
    t = 0
    while(1):
        try:
            gc = gspread.authorize(credentials)
            write_log(get_now() + " Auth success")
            print("Auth success...")
            break
        except gspread.exceptions.AuthenticationError or gspread.exceptions.RequestError:
            write_log(get_now() + " " + str(e1))
            t+=1
            write_log(get_now() + "Try to auth: " + str(t))
            if t == 100:
                # print("Google Auth got problem, program exit...")
                write_log(get_now() + " Google Auth got problem, program exit...")
                sys.exit()
    try:
        sh          = gc.open(spreadsheet_name)
        # print "Success open spreadsheet"
        write_log(get_now() + " Success open spreadsheet")
    except gspread.exceptions.SpreadsheetNotFound as e2:
        # print str(e2) + "\n No spreadsheet name " + spreadsheet_name + "create spreadsheet"
        write_log(get_now() + " " + str(e2) + "\n No spreadsheet name " + spreadsheet_name + "create spreadsheet")
        sh = gc.create(spreadsheet_name)
    sh.share(email, perm_type='user', role='writer')
    return sh

# Open bt sheet and create if not exist
def write_data(spread_sheet_name, di, sheet_name):
    sh = gs_auth(spread_sheet_name)
    try:
        ws = sh.worksheet(sheet_name)
        # print ("sheet " + sheet_name + " exist")
        write_log(get_now() + " sheet " + sheet_name + " exist")

        # Get number of row exist in sheet
        # count = 2
        for i in range(2, 250):
            if ws.cell(i, 1).value != "":
                # print(str(i) + "ko dc")
                pass
            else:
                # print(str(i) + "dc")
                count = i
                # print count
                break
        # Write current date
        ws.update_cell(count, 1, di[sheet_name]["data"]["time"])
        # Append data to exist sheet
        le = len(di[sheet_name]["data"]["pair"])
        while(le > 0):
            sh = gs_auth(spread_sheet_name)
            ws = sh.worksheet(sheet_name)
            cot = 2

            # Lay so cap hien co trong sheet va vi tri cua chung
            l = {}
            i = 2
            while(i < ws.col_count):
                l[ws.cell(1, i).value] = i
                i +=2
            for key, value in di[sheet_name]["data"]["pair"].iteritems():
                try:
                    if key in l:
                        # print(key + " in list")
                        write_log(get_now() + " " + key + " in list")
                        if di[sheet_name]["data"]["pair"][key] != "0":
                            ws.update_cell(count, l[key], value["last_price"])
                            ws.update_cell(count, l[key]+1, value["volume"])
                            di[sheet_name]["data"]["pair"][key] = "0"
                            le = le - 1
                            # print("lenghth: " + str(le))
                        else:
                            print(di[sheet_name]["data"]["pair"][key] + " = 0 , khong ghi")
                            write_log(get_now() + " " + di[sheet_name]["data"]["pair"][key] + " = 0 , khong ghi")
                    else:
                        # print(key + " not in list")
                        write_log(get_now() + " " + key + " NOT in list")
                        ws.add_cols(2)
                        new_cot = ws.col_count - 1
                        write_log(get_now() + " them cot thu " + str(new_cot))
                        # Write new header for new pair
                        ws.update_cell(1, new_cot, key)
                        ws.update_cell(2, new_cot, "Price")
                        ws.update_cell(2, new_cot+1, "Volume")

                        # Write data of pair
                        ws.update_cell(count, new_cot, value["last_price"])
                        ws.update_cell(count, new_cot+1, value["volume"])
                        le = le -1
                        # print("lenghth: " + str(le))
                    cot+= 2
                except gspread.exceptions.RequestError as rqe0:
                    # print("Co van de #1: " + str(rqe0))
                    write_log(get_now() + " Co van de #1: " + str(rqe0))
                    break
    # First record of sheet
    except gspread.exceptions.WorksheetNotFound :

        # print("sheet " + sheet_name + " not exist")
        write_log(get_now() + " sheet " + sheet_name + " not exist")
        ws = sh.add_worksheet(sheet_name, 250, di[sheet_name]["column"])
        # print "created sheet " + sheet_name
        write_log(get_now() + " created sheet " + sheet_name)

        ws.update_cell(2, 1, "Date")
        ws.update_cell(3, 1, di[sheet_name]["data"]["time"])

        cot = 2
        le = len(di[sheet_name]["data"]["pair"])
        while(le > 0):
            sh = gs_auth(spread_sheet_name)
            ws = sh.worksheet(sheet_name)
            # print("auth trong except ko co sheet")
            write_log(get_now() + " auth trong except ko co sheet")
            # Write data of the first record
            for key, value in di[sheet_name]["data"]["pair"].iteritems():
                try:
                    if di[sheet_name]["data"]["pair"][key] != "0":
                        # print("ghi data moi vao sheet moi tao: " + key)
                        write_log(get_now() + " ghi data moi vao sheet moi tao: " + key)
                        ws.update_cell(1, cot, key)
                        ws.update_cell(2, cot, "Price")
                        ws.update_cell(2, cot+1, "Volume")

                        # Write the first record
                        ws.update_cell(3, cot, value["last_price"])
                        ws.update_cell(3, cot+1, value["volume"])
                        write_log(get_now() + " Wrote pair:" + key)

                        di[sheet_name]["data"]["pair"][key] = "0"
                        write_log(get_now() + " Da set gia tri key bang 0")
                        cot = cot + 2
                        le = le -1
                        # print("lenghth: " + str(le))
                    else:
                        pass
                except gspread.exceptions.RequestError as rqe:
                    # print(str(rqe) + " khong ghi duoc")
                    write_log(get_now() + " " + str(rqe) + " khong ghi duoc")
                    break
start_time = datetime.datetime.now()

write_log(get_now() + " Bat dau phien lam viec----------------------------------------------------")
binance = get_binance()
bittrex = get_bittrex()

col_bittrex = len(bittrex["pair"])*2 + 1
col_binance = len(binance["pair"])*2 + 1

bittrex_sheet_name      = get_time()[:7] + "-bittrex"
binance_sheet_name      = get_time()[:7] + "-binance"

bt = {bittrex_sheet_name: {"data": bittrex, "column": col_bittrex}}
bn = {binance_sheet_name: {"data": binance, "column": col_binance}}

write_data("Coin data", bt, bittrex_sheet_name)
write_data("Coin data", bn, binance_sheet_name)
end_time = datetime.datetime.now()
print("Thoi gian chay:"+ str(end_time - start_time))
write_log(get_now() + " Thoi gian chay:"+ str(end_time - start_time))

write_log(get_now() + "Ket thuc phien lam viec----------------------------------------------------")
