from binance.client import Client
from Candle import Candle
from binance.websockets import BinanceSocketManager
import ArbitrageTradingAlgorithm as ATA
import pandas as pd
from CurrencyPair import CurrencyPair
from config import Config, BinanceConfig
import os
from TradingAnalyzeException import TradingAnalyzeException
from logger import Logger
import dateparser as dp


def get_major_currency_path(major_currency):

    start_date = dp.parse(BinanceConfig.TICKERS_GETTER_START_DATE).strftime("%d-%m-%Y")

    end_date = dp.parse(BinanceConfig.TICKERS_GETTER_END_DATE).strftime("%d-%m-%Y")
    major_currency_path = '{0}_{1}_{2}_{3}'.format(major_currency,
                                                   BinanceConfig.TICKERS_GETTER_INTERVAL,
                                                   start_date,
                                                   end_date)

    return major_currency_path


def set_currency_pair_closes(currency_pair, current_currency_pair_path, interval, s_date, e_date, client)-> CurrencyPair:

    first_currency_candles = []
    second_currency_candles = []

    first_currency_closes = []
    second_currency_closes = []
    Logger.log_info(current_currency_pair_path,
             "Получаем с бинанса данные о свечах пар {0} и {1}...".format(currency_pair.first_currency_name,
                                                                          currency_pair.second_currency_name))
    result1 = client.get_historical_klines(currency_pair.first_currency_name, interval, s_date, e_date)
    result2 = client.get_historical_klines(currency_pair.second_currency_name, interval, s_date, e_date)

    Logger.log_info(current_currency_pair_path, "Данные пришли.")
    result1_len = len(result1)
    result2_len = len(result2)

    Logger.log_info(current_currency_pair_path,
             "Кол-во данных по {0}: {1}.".format(currency_pair.first_currency_name, result1_len))
    Logger.log_info(current_currency_pair_path,
             "Кол-во данных по {0}: {1}.".format(currency_pair.second_currency_name, result2_len))

    if result1_len == 0 or result2_len == 0:
        raise TradingAnalyzeException("Данных нет.", current_currency_pair_path,
                                      is_first_currency_closes_empty=result1_len == 0)

    diff = result1_len - result2_len
    diff_percent = 0.0
    is_first_currency_more = False

    if diff > 0:
        diff_percent = abs(diff) / result1_len
        is_first_currency_more = True
    else:
        diff_percent = abs(diff) / result2_len

    if diff_percent > Config.SERIES_DIFFERENCE_PERCENT_THRESHOLD:
        raise TradingAnalyzeException("Данные по валютам слишком отличаются в размерах.", current_currency_pair_path)

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

    currency_pair.first_currency_closes = pd.Series(first_currency_closes)
    currency_pair.second_currency_closes = pd.Series(second_currency_closes)

    return currency_pair


def calculate_cointegration_for_currency_pair(interval, s_date, e_date, currency_pair, log_path,
                                              client) -> CurrencyPair:
    try:
        current_currency_pair_path = '{0}/{1}_{2}'.format(log_path, currency_pair.first_currency_name,
                                                          currency_pair.second_currency_name)

        if not os.path.isdir(current_currency_pair_path):
            os.mkdir(current_currency_pair_path)
        else:
            return currency_pair

        currency_pair = set_currency_pair_closes(currency_pair, current_currency_pair_path,
                                                 interval, s_date, e_date, client)

        return ATA.run(currency_pair, current_currency_pair_path)

    except TradingAnalyzeException as ex:
        Logger.log_info(ex.log_path, ex.message)
        currency_pair.is_first_currency_closes_empty = ex.is_first_currency_closes_empty

    except Exception as ex:
        print(ex)
    finally:
        return currency_pair


def get_grouped_tickers(tickers, major_currencies):
    grouped_tickers = {}

    for major_currency in major_currencies:

        current_tickers = []
        for ticker in tickers:
            if ticker['symbol'].rfind(major_currency) > 0:
                current_tickers.append(ticker['symbol'])

        grouped_tickers.update({major_currency: current_tickers})

    return grouped_tickers


def run():

    major_currencies = ['BTC', 'ETH', 'USDT', 'USDC']

    client = Client(BinanceConfig.API_KEY, BinanceConfig.API_SECRET)

    tickers = client.get_all_tickers()

    grouped_tickers = get_grouped_tickers(tickers, major_currencies)

    interval = BinanceConfig.TICKERS_GETTER_INTERVAL
    start_date = BinanceConfig.TICKERS_GETTER_START_DATE
    end_date = BinanceConfig.TICKERS_GETTER_END_DATE

    for major_currency, gp in grouped_tickers.items():

        major_currency_path = get_major_currency_path(major_currency)
        print("Мажорная валюта: {0}.".format(major_currency))

        if not os.path.isdir(major_currency_path):
            os.mkdir(major_currency_path)

        current_grouped_tickers = gp
        current_tickers_len = len(current_grouped_tickers)

        for i in range(0, current_tickers_len - 1):
            first_currency = current_grouped_tickers.pop()

            for second_currency in current_grouped_tickers:
                currency_pair = CurrencyPair()
                currency_pair.first_currency_name = first_currency
                currency_pair.second_currency_name = second_currency
                # TODO если по first_currency данные не приходят, сделать break
                result_cointegration_currency_pair = calculate_cointegration_for_currency_pair(interval, start_date,
                                                                                               end_date, currency_pair,
                                                                                               major_currency_path,
                                                                                               client)
                if result_cointegration_currency_pair.is_first_currency_closes_empty:
                    break

                # Установим вычеслим объем торгов если пары коинтегрированны
                if result_cointegration_currency_pair.is_stationarity:
                    # TODO понять разницу между quoteVolume и просто volume
                    result_cointegration_currency_pair.set_first_currency_volume(
                        client.get_ticker(symbol=result_cointegration_currency_pair.first_currency_name)
                            .get('quoteVolume'))
                    result_cointegration_currency_pair.set_second_currency_volume(
                        client.get_ticker(symbol=result_cointegration_currency_pair.second_currency_name)
                            .get('quoteVolume'))


run()
