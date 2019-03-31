import os
from os import path as os_path
from config import Config
import json

from objects.CurrencyPair import CurrencyPair


class Logger:
    @staticmethod
    def log_info(path, data):
        if path is not None:
            write_to_file(path, data)
        print(data)

    @staticmethod
    def log_cointegration_info(currency_pair: CurrencyPair, major_currency_path=None):
        log_path = ''

        if major_currency_path is None:
            log_path = os.path.join(Config.LOGGING_PATH, Config.COINTEGRATION_LOG_PATH)
        else:
            log_path = os.path.join(major_currency_path, Config.COINTEGRATION_LOG_PATH)

        if not os.path.isdir(log_path):
            os.mkdir(log_path)

        data = 'Найдена коинтеграция в паре {0}-{1}. Ряд остатков стационарен!'.format(
            currency_pair.first_currency_name,
            currency_pair.second_currency_name)

        write_to_file(log_path, data, Config.COINTEGRATION_INFO_TXT_FILENAME)
        json_data = {}

        with open(os_path.join(log_path, Config.COINTERGRATION_INFO_JSON_FILENAME), 'a+') as json_file:

            if os.stat(json_file.name).st_size == 0:
                json_data = {}
            else:
                json_file.seek(0)
                json_data = json.load(json_file)

        with open(os_path.join(log_path, Config.COINTERGRATION_INFO_JSON_FILENAME), 'w') as json_file:
            if 'cointegration_pairs' not in json_data:
                json_data['cointegration_pairs'] = {}

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

            json_data['cointegration_pairs'][pair_in_str] = info_pair

            # устанавливаем на начало, перезаписывая весь файл
            json_file.seek(0)
            json.dump(json_data, json_file, ensure_ascii=False)
            json_file.truncate()


def write_to_file(path, data, filename='log.txt'):
    file = open(os_path.join(path, filename), 'a+')
    file.write(data + '\n')
    file.close()
