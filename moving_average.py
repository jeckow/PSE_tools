'''
This is a simple code for a technical analysis tool where we use moving averages
(a 200-day and 50-day moving average) to identify specific crossovers
such as golden crosses (buy signals) and death crosses (selling signals)
and determine whether to buy or sell stocks
'''

import requests
from datetime import datetime
import json
import pandas as pd

# set date range
start_date = '2020-08-13'
end_date = datetime.today().strftime('%Y-%m-%d')
date_list = pd.date_range(start=start_date, end=end_date).to_list()

# pull the price data using phisix-api
stock_price = []
for date in date_list:
    str_date = date.strftime('%Y-%m-%d')
    url = f"http://phisix-api.appspot.com/stocks/AREIT.{str_date}.json"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    if len(response.text) == 0:
        pass
    
    else:
        stock_info = json.loads(response.text)
        stock_price.append(stock_info['stock'][0]['price']['amount'])
        print(stock_info['stock'][0]['price']['amount'])
