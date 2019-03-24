import os
from os import path as os_path
from config import Config
import json

from CurrencyPair import CurrencyPair

class Logger:
    @staticmethod
    def log_info(path, data):
        write_to_file(path, data)
        print(data)

    @staticmethod
    def log_cointegration_info(currency_pair: CurrencyPair):
        if not os.path.isdir(Config.COINTEGRATION_LOG_PATH):
            os.mkdir(Config.COINTEGRATION_LOG_PATH)

        data = 'Найдена коинтеграция в паре {0}-{1}. Ряд остатков стационарен!'.format(
            currency_pair.first_currency_name,
            currency_pair.second_currency_name)

        write_to_file(Config.COINTEGRATION_LOG_PATH, data, Config.COINTEGRATION_INFO_TXT_FILENAME)

        with open(os_path.join(Config.COINTEGRATION_LOG_PATH, Config.COINTERGRATION_INFO_JSON_FILENAME),
                  'r+') as json_file:
            json_data = json.load(json_file)
            if 'cointegrated_pairs' not in json_data:
                json_data['cointegrated_pairs'] = {}

            pair_in_str = '{0}_{1}'.format(currency_pair.first_currency_name, currency_pair.second_currency_name)

            info_pair = {
                '{0}_closes_amount'.format(currency_pair.first_currency_name): len(
                        currency_pair.first_currency_closes),
                '{0}_closes_amount'.format(currency_pair.second_currency_name): len(
                        currency_pair.second_currency_closes),
                '{0}_volume'.format(currency_pair.first_currency_name):
                    currency_pair.first_currency_volume,
                '{0}_volume'.format(currency_pair.second_currency_name):
                        currency_pair.second_currency_volume
            }

            json_data['cointegrated_pairs'][pair_in_str] = info_pair

            # устанавливаем на начало, перезаписывая весь файл
            json_file.seek(0)
            json.dump(json_data, json_file, ensure_ascii=False)


def write_to_file(path, data, filename='log.txt'):
    file = open(os_path.join(path, filename), 'a+')
    file.write(data + '\n')
    file.close()