import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ArbitrageTradingAlgorithm as ATA
import os
import json
from CurrencyPair import CurrencyPair
from TradingAnalyzeException import TradingAnalyzeException

# # Length of series
# N = 100
#
# # Generate a stationary random X1
# X1 = np.random.normal(0, 1, N)
# # Integrate it to make it I(1)
# X1 = np.cumsum(X1)
# X1 = pd.Series(X1)
# X1.name = 'X1'
#
# # Make an X2 that is X1 plus some noise
# X2 = X1 + np.random.normal(0, 1, N)
# X2.name = 'X2'
#
# plt.plot(X1)
# plt.plot(X2)
# plt.xlabel('Time')
# plt.ylabel('Series Value')
# plt.legend([X1.name, X2.name])
# plt.show()
#
# Z = X2.diff()[1:]
# Z.name = 'Z'
#
# ATA.check_for_stationarity(Z);
#
# end = '2017-01-01'
# start = '2011-01-01'
# symbols = ['MSFT','ADBE']
# data = dl.load_data_nologs('nasdaq', symbols , start, end)['ADJ CLOSE']
#
# X1 = data['MSFT']
# X2 = data['ADBE']
#
# plt.plot(X1)
# plt.plot(X2)
# plt.xlabel('Time')
# plt.ylabel('Series Value')
# plt.legend([X1.name, X2.name])
# plt.show()
#
# X1 = sm.add_constant(X1)
# results = sm.OLS(X2, X1).fit()
#
# # Get rid of the constant column
# X1 = X1['MSFT']
#
# results.params
#
# b = results.params['MSFT']
# Z = X2 - b * X1
# Z.name = 'Z'
#
# plt.plot(Z.index, Z.values)
# plt.xlabel('Time')
# plt.ylabel('Series Value')
# plt.legend([Z.name])
# plt.show()
#
# ATA.check_for_stationarity(Z);

cur = 'ETH'
pair1 = 'XRPETH'
pair2 = 'ETHUSDT'
pair3 = 'BTCUSDT'

#
# print(pair1.rfind(cur))
# print(pair2.rfind(cur))
# print(pair3.rfind(cur))
#
# arr = [pair1, pair2, pair3]
# print(arr)
# print(arr.pop())
# print(arr)
#
# X1 = np.random.normal(0, 1, 100)
# # # Integrate it to make it I(1)
# X1 = np.cumsum(X1)
# xs = np.linspace(1,100,len(X1))
#
# plt.plot(np.repeat(-1, len(X1)), 'r--')
# plt.plot(np.repeat(1, len(X1)), 'y--')
# plt.plot(X1, color='blue')
# plt.show()

# data = {}
# data['people'] = []
# data['people'].append({
#     'name': 'Scott',
#     'website': 'stackabuse.com',
#     'from': 'Nebraska'
# })
# data['people'].append({
#     'name': 'Larry',
#     'website': 'google.com',
#     'from': 'Michigan'
# })
# data['people'].append({
#     'name': 'Tim',
#     'website': 'apple.com',
#     'from': 'Alabama'
# })
data = {}

# with open('data.json', 'r+') as json_file:
#     data = json.load(json_file)
#     if 'column' not in data:
#         data['column'] = []
#     data['column'].append({
#         '12': '2'
#     })
#     json.dump(data, json_file)

#with open('data.json', 'w') as json_file:
try:
    currency_pair = CurrencyPair()
    currency_pair.first_currency_name = 'kek'
    print(currency_pair.first_currency_name)
    print(currency_pair.second_currency_name)
    raise TradingAnalyzeException("тут шо-то происходит", "path")

except TradingAnalyzeException as ex:
    print(ex.message)
    print(ex.log_path)