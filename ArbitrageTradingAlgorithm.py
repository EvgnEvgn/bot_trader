import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller
import os
from config import Config


def check_for_stationarity(X, cutoff=0.01):
    # We must observe significant p-value to convince ourselves that the series is stationary
    pvalue = adfuller(X)[1]
    if pvalue < cutoff:
        return True
    else:
        return False


def get_z_score(currency_pair, log_path):
    x = sm.add_constant(currency_pair.first_currency_closes)
    y = currency_pair.second_currency_closes
    model = sm.OLS(y, x).fit()

    resid = model.resid

    is_stationarity = check_for_stationarity(resid)

    if log_path is not None:

        plt.plot(resid, color='blue')
        plt.title("Residuals of pairs: {0} and {1}".format(currency_pair.first_currency_name, currency_pair.second_currency_name))

        plt.savefig('{0}/{1}{2}_residuals.png'.format(log_path, currency_pair.first_currency_name, currency_pair.second_currency_name))
        plt.clf()
        log_info(log_path, "Ряд остатков валютных пар {0} и {1} является {2}".format(currency_pair.first_currency_name, currency_pair.second_currency_name, get_stationarity_state(is_stationarity)))

    if not is_stationarity:
        return

    b = model.params[0]

    x = currency_pair.first_currency_closes

    y = currency_pair.second_currency_closes

    residual = y - b*x

    z = (residual - np.mean(residual)) / np.std(residual)

    # получаем числовые константы
    z_upper_limit = np.mean(z) + np.std(z)
    z_lower_limit = np.mean(z) - np.std(z)

    log_cointegration_info(currency_pair)
    plt.plot(z, color='black')
    plt.plot(np.repeat(z_upper_limit, len(z)), 'r--')
    plt.plot(np.repeat(z_lower_limit,     len(z)), 'y--')
    plt.savefig('{0}/{1}{2}_z_with_limits.png'.format(log_path, currency_pair.first_currency_name, currency_pair.second_currency_name))
    plt.clf()

    log_info(log_path, 'Z = {0}.\n z_upper_limit = {1}.\n z_lower_limit = {2}'.format(z, z_upper_limit, z_lower_limit))

    return z, z_upper_limit, z_lower_limit


def run(currency_pair, log_path=None):
    print("Выполняется проверка коинтеграции валютных пар {0} и {1}.".format(currency_pair.first_currency_name, currency_pair.second_currency_name))

    is_stationarity_first_currency = check_for_stationarity(currency_pair.first_currency_closes)
    is_stationarity_second_currency = check_for_stationarity(currency_pair.second_currency_closes)

    if log_path is not None:

        log_info(log_path, get_stationarity_state_info(currency_pair.first_currency_name, is_stationarity_first_currency))
        log_info(log_path, get_stationarity_state_info(currency_pair.second_currency_name, is_stationarity_second_currency))

    if is_stationarity_first_currency or is_stationarity_second_currency:
        return False

    get_z_score(currency_pair, log_path)

    #Алгоритм открытий и закрытий позиций по валютам


def write_to_file(path, data, filename='log.txt'):
    file = open('{0}/{1}'.format(path, filename), 'a+')
    file.write(data + '\n')
    file.close()


def get_stationarity_state_info(name, is_stationarity=False, ):

    state = get_stationarity_state(is_stationarity)
    return 'Пара {0} имеет {1} ряд.'.format(name, state)


def get_stationarity_state(is_stationarity=False):

    stationarity_in_string = "стационарный"
    non_stationarity_in_string = "нестационарный"

    return stationarity_in_string if is_stationarity else non_stationarity_in_string


def log_info(path, data):
    write_to_file(path, data)
    print(data)


def log_cointegration_info(currency_pair):
    if not os.path.isdir(Config.COINTEGRATION_LOG_PATH):
        os.mkdir(Config.COINTEGRATION_LOG_PATH)

    data = 'Найдена коинтеграция в паре {0}-{1}. Ряд остатков стационарен!'.format(currency_pair.first_currency_name, currency_pair.second_currency_name)
    write_to_file(Config.COINTEGRATION_LOG_PATH, data, 'log_cointegration_info.txt')

