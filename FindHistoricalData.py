import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from datetime import datetime

def get_companies(ex="NASDAQ"):
    url = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange={}&render=download"
    url = url.format(ex)
    return pd.read_csv(url)

start_date = datetime(2016,1,1)
end_date = datetime.today()
prices = web.DataReader('AAPL', 'yahoo', start_date, end_date)

# print(prices.shape)
# print("-----------------------")
# print(prices.describe())
# print("-----------------------")
# print(prices.head(3))
# print("-----------------------")
# print(prices.tail(3))
# print("-----------------------")
# print(prices.columns)
# print("-----------------------")
# print(prices.index)
# print("-----------------------")
# print(prices.info)
# print(prices.loc['2015-12-31'][1])


prices[['Close','Volume']].plot(subplots = True, figsize = (10, 8))
plt.legend(loc='best')