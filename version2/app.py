from binance.client import Client
import pandas as pd
import numpy as np
from scipy.stats.stats import pearsonr
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import json
import pika

class Candle:
    def __init__(self, args):
        self.openTime = args['time']
        self.open = args['open']
        self.high = args['high']
        self.low = args['low']
        self.close = float(args['close'])
        self.volume = float(args['volume'])
        self.closeTime = args['closeTime']
        self.quoteAssetVolume = args['assetVolume']
        self.numberOfTrades = args['trades']
        self.takerBuyBaseAssetVolume = args['buyBaseVolume']
        self.takerBuyQuoteAssetVolume = args['buyAssetVolume']
        self.ignore = args['ignored']



connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='NEED_ANALYZE_PAIR', durable=True)
channel.queue_declare(queue='RESULT_ANALYZE_PAIR', durable=True)

connected = []
old_z = '0'


def check_correlation(firstCurrencyCloses, secondCurrencyCloses):
    if firstCurrencyCloses.empty or secondCurrencyCloses.empty:
        print("No data.")
    else:
        correlation = pearsonr(firstCurrencyCloses, secondCurrencyCloses)
        print(correlation)
        print(np.corrcoef(firstCurrencyCloses, secondCurrencyCloses))
        print('Коефицент кореляции Пирсона: ', correlation[0])


def check_for_stationarity(X, cutoff=0.01):
    # https://habr.com/ru/post/207160/
    # https://www.machinelearningmastery.ru/time-series-data-stationary-python/
    if adfuller(X)[0] > adfuller(X)[4]['5%']:
        print('есть единичные корни, ряд не стационарен')
        return True
    else:
        print('единичных корней нет, ряд стационарен')
        return False
    # We must observe significant p-value to convince ourselves that the series is stationary
    # pvalue = adfuller(X)[1]
    # if pvalue < cutoff:
    #     return True
    # else:
    #     return False


def get_stationarity_state(is_stationarity=False):
    stationarity_in_string = "стационарный"
    non_stationarity_in_string = "нестационарный"

    return stationarity_in_string if is_stationarity else non_stationarity_in_string


def plot_residuals(residuals):
    plt.clf()
    plt.plot(residuals, color='blue')
    plt.show()


def set_z_score(firstCurrencyCloses, secondCurrencyCloses):
    x = sm.add_constant(secondCurrencyCloses)
    y = firstCurrencyCloses
    model = sm.OLS(y, x).fit()

    resid = model.resid

    is_resid_stationarity = check_for_stationarity(resid)

    plot_residuals(resid)
    print("Ряд остатков валютных пар является {0}".format(get_stationarity_state(is_resid_stationarity)))

    if is_resid_stationarity:
        b = model.params[0]

        x = secondCurrencyCloses

        y = firstCurrencyCloses

        residual = y - b * x
        #residual = secondCurrencyCloses / firstCurrencyCloses

        z = (residual - np.mean(residual)) / np.std(residual)

        # получаем числовые константы
        z_upper_limit = np.mean(z) + np.std(z)
        z_lower_limit = np.mean(z) - np.std(z)

    return z, z_upper_limit, z_lower_limit


def analysisPair(firstCurrencyData, secondCurrencyData):
    firstCurrencyData = list(map(lambda x: Candle(x), firstCurrencyData))
    secondCurrencyData = list(map(lambda x: Candle(x), secondCurrencyData))

    firstCurrencyClosesList = list(map(lambda x: x.close, firstCurrencyData))
    secondCurrencyClosesList = list(map(lambda x: x.close, secondCurrencyData))

    firstCurrencyCloses = pd.Series(firstCurrencyClosesList)
    secondCurrencyCloses = pd.Series(secondCurrencyClosesList)

    print('Кол-во данных для первой валюты: ' + str(len(firstCurrencyCloses)))
    print('Кол-во данных для второй валюты: ' + str(len(secondCurrencyCloses)))

    # TODO
    if (len(firstCurrencyCloses) != len(secondCurrencyCloses)):
        return

    is_stationarity_first_currency = check_for_stationarity(firstCurrencyCloses)
    is_stationarity_second_currency = check_for_stationarity(secondCurrencyCloses)

    # check_correlation(firstCurrencyCloses, secondCurrencyCloses)
    print('Коефицент кореляции: ', firstCurrencyCloses.corr(secondCurrencyCloses))

    (z, z_upper_limit, z_lower_limit) = set_z_score(firstCurrencyCloses, secondCurrencyCloses)

    last_z_value = z[len(z) - 1]
    strZ = str(last_z_value)

    print('_____Z: ' + str(last_z_value))
    plt.plot(z, color='black')
    plt.plot(np.repeat(z_upper_limit, len(z)), 'r--')
    plt.plot(np.repeat(z_lower_limit, len(z)), 'y--')
    plt.show()
    # plt.plot((secondCurrencyCloses / firstCurrencyCloses), color='black')
    # plt.axhline((secondCurrencyCloses / firstCurrencyCloses).mean(), color='red', linestyle='--')


    return z.tolist(), \
           z_upper_limit, \
           z_lower_limit, \
           list(map(lambda x: x.closeTime, firstCurrencyData)), \
           firstCurrencyClosesList, \
           secondCurrencyClosesList

def callback(ch, method, properties, body):
    bodyParse = json.loads(body)
    z, z_upper_limit, z_lower_limit, time, price1, price2 =  analysisPair(bodyParse['firstCurrencyData'], bodyParse['secondCurrencyData'])


    sendDataQMQP = {}
    sendDataQMQP['z_data'] = {}
    sendDataQMQP['messageId'] = ''
    sendDataQMQP['z_data']['z'] = z
    sendDataQMQP['z_data']['z_upper_limit'] = z_upper_limit
    sendDataQMQP['z_data']['z_lower_limit'] = z_lower_limit
    sendDataQMQP['z_data']['time'] = time
    sendDataQMQP['z_data']['price1'] = price1
    sendDataQMQP['z_data']['price2'] = price2
    sendDataQMQP['messageId'] = bodyParse['messageId']

    channel.basic_publish(exchange='',
                          routing_key='RESULT_ANALYZE_PAIR',
                          body=json.dumps(sendDataQMQP))


channel.basic_consume(queue='NEED_ANALYZE_PAIR',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
