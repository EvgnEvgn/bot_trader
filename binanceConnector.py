from binance.client import Client
from Candle import Candle
from binance.websockets import BinanceSocketManager
import ArbitrageTradingAlgorithm as ATA
import pandas as pd
from CurrencyPair import CurrencyPair
import config
import os


def write_to_file(path, data, filename='log.txt'):
    file = open('{0}/{1}'.format(path, filename), 'a+')
    file.write(data + '\n')
    file.close()


def log_info(path, data):
    write_to_file(path, data)
    print(data)


def search_cointegrated_currency_pairs(interval, s_date, e_date, currency_pair, log_path):
    first_currency_candles = []
    second_currency_candles = []

    first_currency_closes = []
    second_currency_closes = []

    current_currency_pair_path = '{0}/{1}_{2}'.format(log_path, currency_pair[0], currency_pair[1])

    if not os.path.isdir(current_currency_pair_path):
        os.mkdir(current_currency_pair_path)

    print("Получаем с бинанса данные о свечах пар {0} и {1}...".format(currency_pair[0], currency_pair[1]))
    result1 = client.get_historical_klines(currency_pair[0], interval, s_date, e_date)
    result2 = client.get_historical_klines(currency_pair[1], interval, s_date, e_date)

    print("Данные пришли.")
    result1_len = len(result1)
    result2_len = len(result2)

    print("Кол-во данных по {0}: {1}.".format(currency_pair[0], result1_len))
    print("Кол-во данных по {0}: {1}.".format(currency_pair[1], result2_len))

    diff = result1_len - result2_len
    diff_percent = 0.0
    is_first_currency_more = False

    if diff > 0:
        diff_percent = abs(diff) / result1_len
    else:
        diff_percent = abs(diff) / result2_len

    if diff_percent > config.Config.SERIES_DIFFERENCE_PERCENT_THRESHOLD:
        log_info(current_currency_pair_path, "Данные по валютам отличаются в размерах.")
        return

    elif is_first_currency_more:
        result1 = result1[abs(diff):]
    else:
        result2 = result2[abs(diff):]

    for i in range(0, len(result1) - 1):
        first_currency_candle = Candle(result1[i])
        second_currency_candle = Candle(result2[i])

        first_currency_candles.append(first_currency_candle)
        second_currency_candles.append(second_currency_candle)

        first_currency_closes.append(first_currency_candle.close)
        second_currency_closes.append(second_currency_candle.close)

    first_currency_closes, second_currency_closes = pd.Series(first_currency_closes), pd.Series(second_currency_closes)

    currency_pair = CurrencyPair(currency_pair[0], first_currency_closes, currency_pair[1], second_currency_closes)

    ATA.run(currency_pair, current_currency_pair_path)


def get_grouped_tickers(tickers, major_currencies):
    grouped_tickers = {}

    for major_currency in major_currencies:

        current_tickers = []
        for ticker in tickers:
            if ticker['symbol'].rfind(major_currency) > 0:
                current_tickers.append(ticker['symbol'])

        grouped_tickers.update({major_currency: current_tickers})

    return grouped_tickers


major_currencies = ['BTC', 'ETH', 'USDT', 'USDC']

client = Client(config.BinanceConfig.API_KEY, config.BinanceConfig.API_SECRET)

tickers = client.get_all_tickers()

grouped_tickers = get_grouped_tickers(tickers, major_currencies)

interval = '15m'
start_date = '2019-02-23 15:00 UTC'
end_date = '2019-03-23 15:00 UTC'

for major_currency, gp in grouped_tickers.items():
    major_currency_path = '{0}/{1}'.format(config.Config.LOGGING_PATH, major_currency)
    print("Мажорная валюта: {0}.".format(major_currency))

    if not os.path.isdir(major_currency_path):
        os.mkdir(major_currency_path)

    current_grouped_tickers = gp
    current_tickers_len = len(current_grouped_tickers)

    for i in range(0, current_tickers_len - 1):
        first_currency = current_grouped_tickers.pop()

        for second_currency in current_grouped_tickers:
            search_cointegrated_currency_pairs(interval, start_date, end_date, (first_currency, second_currency), major_currency_path)


