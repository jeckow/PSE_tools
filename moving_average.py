'''
This is a simple implementation of aa 200-day and 50-day moving average for
identifying golden crosses (buy signals) and death crosses (selling signals)

Curretly PSEI API is does not work so the candlestick graph cannot be
implemented yet. Hence a different API is used just for visualizing
the moving averages
'''

import matplotlib.pyplot as plt
from datetime import datetime
import dask.delayed as de
import pandas as pd
import numpy as np
import requests
import json


# set date range
start_date = '2020-08-13'
end_date = datetime.today().strftime('%Y-%m-%d')
date_list = pd.date_range(start=start_date, end=end_date).to_list()

# set stock symbol to monitor
ticker = 'AREIT'


# pull the data using phisix-api
def get_data(date_list, stock_symbol):
    stock_price = []
    stock_dates = []
    for date in date_list:
        str_date = date.strftime('%Y-%m-%d')
        url = f"http://phisix-api.appspot.com/stocks/{ticker}.{str_date}.json"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
    
        if len(response.text) == 0:
            pass
        
        else:
            stock_info = json.loads(response.text)
            stock_dates.append(date.date())
            stock_price.append(stock_info['stock'][0]['price']['amount'])
            print(stock_price[-1], stock_dates[-1])
            
       
    return [stock_price, stock_dates]


def combine(data_1, data_2, dates_1, dates_2):
    data_1.extend(data_2)
    dates_1.extend(dates_2)
    
    return data_1, dates_1

stock_data_1 = de(get_data)(date_list[:126], ticker)
stock_data_2 = de(get_data)(date_list[126:], ticker)

print('pulling data...')
stock_data = de(combine)(stock_data_1[0], stock_data_2[0], stock_data_1[1], stock_data_2[1]).compute()
print('done')


prices = np.array(stock_data).T
df = pd.DataFrame(prices)
df.columns = ['close', 'date']

mean_50 = df.close.rolling(window=50).mean()
mean_200 = df.close.rolling(window=200).mean()

plt.plot(df.date, df.close, label=f'{ticker}')
plt.plot(df.date, mean_50, label='50-day SMA', color='red')
plt.plot(df.date, mean_200, label='200-day SMA', color='yellow')
plt.legend(loc='upper left')
plt.show()