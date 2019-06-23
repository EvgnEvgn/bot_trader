import numpy as np


def logarithm_currency_pair(func):
    def wrapper(*args, **kwargs):
        currency_pair_info = func(*args, **kwargs)

        currency_pair_info.first_currency_closes = np.log(currency_pair_info.first_currency_closes)
        currency_pair_info.second_currency_closes = np.log(currency_pair_info.second_currency_closes)

        return currency_pair_info
    return wrapper


def add_correlation_info(func):
    def wrapper(*args, **kwargs):
        currency_pair_info = func(*args, **kwargs)

        currency_pair_info.first_currency_closes = np.log(currency_pair_info.first_currency_closes)
        currency_pair_info.second_currency_closes = np.log(currency_pair_info.second_currency_closes)

        return currency_pair_info
    return wrapper