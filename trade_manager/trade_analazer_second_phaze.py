import json
import os
import schedule
import time
import random
import numpy as np
import json
import datetime
import dateparser as dp
import matplotlib.pyplot as plt
import pickle
from os import path as os_path
from config import Config, BinanceConfig, RedisConfig
from objects.CurrencyPair import CurrencyPair
from cointegration_analyzer.currency_pair_cointegration_analyzer import set_currency_pair_info
from trading_algorithms.ArbitrageTradingAlgorithm import set_z_score
from objects.trade_state import TradeState
from objects.trade_state_position import TradeStatePosition
from trade_manager.trade_stub_manager import TradeManagerStub
from objects.wallet import Wallet
from Loggers.logger import Logger
from objects.RedisClientSingleton import RedisClientSingleton as RedisClient
from objects.BinanceClientSingleton import BinanceClientSingleton as BinanceClient

redis = RedisClient().get_client()


def get_major_currency(pairs_value):
    return pairs_value.split('_')[0]


def get_minor_currency(pairs_value):
    return pairs_value.split('_')[1]


def sort_by_volume(x):
    return x[1][get_major_currency(x[0]) + '_volume'] + x[1][get_minor_currency(x[0]) + '_volume']


def read_log_cointegration_info():
    with open(os_path.join(Config.COINTEGRATION_LOG_PATH, Config.COINTERGRATION_INFO_JSON_FILENAME),
              'r+') as json_file:
        return json.load(json_file)


def get_currency_path(folder_name='GG_WP'):
    start_date = dp.parse(BinanceConfig.TICKERS_GETTER_START_DATE_5M).strftime("%d-%m-%Y")

    end_date = dp.parse(BinanceConfig.TICKERS_GETTER_END_DATE_15M).strftime("%d-%m-%Y")
    major_currency_path = '{0}/{1}_{2}_{3}_{4}'.format(Config.LOGGING_PATH,
                                                       folder_name,
                                                       BinanceConfig.TICKERS_GETTER_INTERVAL_5M,
                                                       start_date,
                                                       end_date)

    return major_currency_path


def sort_by_five_minutes():
    log_cointegration_info = read_log_cointegration_info()

    sorted_log_cointegration_info = sorted(log_cointegration_info['cointegrated_pairs'].items(),
                                           key=sort_by_volume)
    for kv in sorted_log_cointegration_info:
        print(kv[0] + ': ' + str(kv[1][get_major_currency(kv[0]) + '_volume']) +
              ': ' + str(kv[1][get_minor_currency(kv[0]) + '_volume']))

    last_five_sorted_log_cointegration_info = sorted_log_cointegration_info[-5:]

    return last_five_sorted_log_cointegration_info


major_currency_name = 'BTC'
mainPairs = 'RVNBTC_XRPBTC'


def init_wallet() -> Wallet:
    wallet = Wallet()
    wallet.add_currency_account('RVN', 100)
    wallet.add_currency_account('XRP', 100)
    wallet.add_currency_account(major_currency_name, 1)

    wallet_redis = redis.get(RedisConfig.TEST_WALLET_KEY + mainPairs)
    if wallet_redis is not None:
        wallet = pickle.loads(wallet_redis)

    return wallet


def init_trade_state() -> TradeState:
    trade_state_redis = redis.get(RedisConfig.TRADE_STATE_KEY + mainPairs)
    ret_trade_state = TradeState()

    if trade_state_redis is not None:
        ret_trade_state = pickle.loads(trade_state_redis)
    return ret_trade_state


trade_manager_stub = TradeManagerStub(init_wallet())
trade_state = init_trade_state()


def job():
    currency_pair = CurrencyPair()
    currency_pair.major_currency_name = major_currency_name
    currency_pair.first_currency_name = get_major_currency(mainPairs)
    currency_pair.second_currency_name = get_minor_currency(mainPairs)

    interval = BinanceConfig.TICKERS_GETTER_INTERVAL_5M
    s_date = BinanceConfig.TICKERS_GETTER_START_DATE_5M
    e_date = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    currency_pair = set_currency_pair_info(currency_pair, interval, s_date, e_date)
    client = BinanceClient().get_client()
    result_currency_pair = set_z_score(currency_pair)

    z = result_currency_pair.z

    last_z_value = z[len(z) - 1]

    # last_z_value = z_array[random.randint(0, len(z_array)-1)]
    # print('_____Z: ' + str(last_z_value))
    Logger.log_info('C:/ArbitrageTrading/log_check_strategy', '_____Z: ' + str(last_z_value))

    # TODO учесть цену если колво валюты меньше чем послдние значение в стакане
    tiker_info = client.get_ticker(symbol=currency_pair.first_currency_name)
    currency_pair.first_currency_market_sell_price = float(tiker_info.get('askPrice'))
    currency_pair.first_currency_market_purchase_price = float(tiker_info.get('bidPrice'))

    Logger.log_info('C:/ArbitrageTrading/log_check_strategy',
                    'Name: ' + currency_pair.first_currency_name +
                    '; purchase_price: ' + str(currency_pair.first_currency_market_purchase_price) +
                    '; sell_price: ' + str(currency_pair.first_currency_market_sell_price))
    # print(
    #     'Name: ' + currency_pair.first_currency_name +
    #     '\npurchase_price: ' + str(currency_pair.first_currency_market_purchase_price)+
    #     '\nsell_price: ' + str(currency_pair.first_currency_market_sell_price))

    tiker_info = client.get_ticker(symbol=currency_pair.second_currency_name)
    currency_pair.second_currency_market_sell_price = float(tiker_info.get('askPrice'))
    currency_pair.second_currency_market_purchase_price = float(tiker_info.get('bidPrice'))

    Logger.log_info('C:/ArbitrageTrading/log_check_strategy',
                    'Name: ' + currency_pair.second_currency_name +
                    '; purchase_price: ' + str(currency_pair.second_currency_market_purchase_price) +
                    '; sell_price: ' + str(currency_pair.second_currency_market_sell_price))

    # print(
    #     'Name: ' + currency_pair.second_currency_name +
    #     '\npurchase_price: ' + str(currency_pair.second_currency_market_purchase_price) +
    #     '\nsell_price: ' + str(currency_pair.second_currency_market_sell_price))

    currency_pair.first_currency_name = currency_pair.first_currency_name \
        .replace(currency_pair.major_currency_name, '')
    currency_pair.second_currency_name = currency_pair.second_currency_name \
        .replace(currency_pair.major_currency_name, '')

    # # TODO убрать
    # result_currency_pair = currency_pair
    # result_currency_pair.z_upper_limit = 1
    # result_currency_pair.z_lower_limit = -1

    if trade_state.trade_state_position == TradeStatePosition.CLOSED:
        if last_z_value > result_currency_pair.z_upper_limit:
            trade_manager_stub.open_high_position(currency_pair, 50, 50, BinanceConfig.COMMISSION, trade_state)
        if last_z_value < result_currency_pair.z_lower_limit:
            trade_manager_stub.open_low_position(currency_pair, 50, 50, BinanceConfig.COMMISSION, trade_state)
    else:
        if (trade_state.trade_state_position == TradeStatePosition.HIGH_OPENED and last_z_value < 0.03) or (
                trade_state.trade_state_position == TradeStatePosition.LOW_OPENED and last_z_value > -0.03):
            trade_manager_stub.close_position(currency_pair, trade_state)

    redis.set(RedisConfig.TRADE_STATE_KEY + mainPairs, pickle.dumps(trade_state))
    redis.set(RedisConfig.TEST_WALLET_KEY + mainPairs, pickle.dumps(trade_manager_stub.wallet))

    Logger.log_info('C:/ArbitrageTrading/log_check_strategy', str(trade_manager_stub.wallet.currency_accounts) + '\n')
    # print('Wallet: ')
    # print(trade_manager_stub.wallet.currency_accounts)
    # plt.plot(z, color='black')
    # plt.plot(np.repeat(result_currency_pair.z_upper_limit, len(z)), 'r--')
    # plt.plot(np.repeat(result_currency_pair.z_lower_limit, len(z)), 'y--')
    # plt.show()


schedule.every(60).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
