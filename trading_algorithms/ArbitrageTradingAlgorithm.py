import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from Loggers.logger import Logger
from objects.CurrencyPair import CurrencyPair
from config import Config


def check_for_stationarity(X, cutoff=0.01):
    # We must observe significant p-value to convince ourselves that the series is stationary
    pvalue = adfuller(X)[1]
    if pvalue < cutoff:
        return True
    else:
        return False


def plot_closes(plot_path, currency_pair: CurrencyPair):
    plt.clf()
    plt.plot(currency_pair.first_currency_closes, color='blue')
    plt.plot(currency_pair.second_currency_closes, color='red')
    plt.title("Residues of pairs: {0} and {1}".format(currency_pair.first_currency_name,
                                                      currency_pair.second_currency_name))
    plt.legend([currency_pair.first_currency_name, currency_pair.second_currency_name])

    plt.savefig('{0}/{1}{2}_{3}'.format(plot_path,
                                        currency_pair.first_currency_name,
                                        currency_pair.second_currency_name,
                                        Config.CLOSES_CHART_FILENAME), figsize=(20, 10), dpi=350)
    plt.close()


def plot_residuals(plot_path, currency_pair: CurrencyPair, residuals):
    plt.clf()
    plt.plot(residuals, color='blue')
    plt.title("Residues of pairs: {0} and {1}".format(currency_pair.first_currency_name,
                                                      currency_pair.second_currency_name))

    plt.savefig('{0}/{1}{2}_{3}'.format(plot_path,
                                        currency_pair.first_currency_name,
                                        currency_pair.second_currency_name,
                                        Config.RESIDUES_RESULT_FILENAME), figsize=(20, 10), dpi=350)
    plt.close()


def plot_z_orders_with_limits(z_orders, z_upper_limit, z_lower_limit, log_path, currency_pair):
    plt.clf()
    plt.plot(z_orders, color='black')
    plt.plot(np.repeat(z_upper_limit, len(z_orders)), 'r--')
    plt.plot(np.repeat(z_lower_limit, len(z_orders)), 'y--')
    plt.savefig('{0}/{1}{2}_z_with_limits.png'.format(log_path, currency_pair.first_currency_name,
                                                      currency_pair.second_currency_name), figsize=(20, 10), dpi=350)
    plt.close()


def set_z_score(currency_pair: CurrencyPair, log_path: str = None) -> CurrencyPair:
    x = sm.add_constant(currency_pair.first_currency_closes)
    y = currency_pair.second_currency_closes
    model = sm.OLS(y, x).fit()

    resid = model.resid

    is_resid_stationarity = check_for_stationarity(resid)

    currency_pair.is_stationarity = is_resid_stationarity

    if log_path is not None:
        plot_closes(log_path, currency_pair)
        plot_residuals(log_path, currency_pair, resid)

        Logger.log_info(log_path,
                        "Ряд остатков валютных пар {0} и {1} является {2}".format(currency_pair.first_currency_name,
                                                                                  currency_pair.second_currency_name,
                                                                                  get_stationarity_state(
                                                                                      is_resid_stationarity)))
    if is_resid_stationarity:
        b = model.params[0]

        x = currency_pair.first_currency_closes

        y = currency_pair.second_currency_closes

        residual = y - b * x

        z = (residual - np.mean(residual)) / np.std(residual)

        # получаем числовые константы
        z_upper_limit = np.mean(z) + np.std(z)
        z_lower_limit = np.mean(z) - np.std(z)

        currency_pair.z = z
        currency_pair.z_upper_limit = z_upper_limit
        currency_pair.z_lower_limit = z_lower_limit

        # Logger.log_cointegration_info(currency_pair)
        # plot_z_orders_with_limits(z, z_upper_limit, z_lower_limit, log_path, currency_pair)

        Logger.log_info(log_path,
                        'z_upper_limit = {0}.\n z_lower_limit = {1}'.format(z_upper_limit, z_lower_limit))

    return currency_pair


def run(currency_pair: CurrencyPair, log_path: str = None) -> CurrencyPair:
    print("Выполняется проверка коинтеграции валютных пар {0} и {1}.".format(currency_pair.first_currency_name,
                                                                             currency_pair.second_currency_name))

    is_stationarity_first_currency = check_for_stationarity(currency_pair.first_currency_closes)
    is_stationarity_second_currency = check_for_stationarity(currency_pair.second_currency_closes)

    if log_path is not None:
        Logger.log_info(log_path,
                        get_stationarity_state_info(currency_pair.first_currency_name,
                                                    is_stationarity_first_currency))
        Logger.log_info(log_path,
                        get_stationarity_state_info(currency_pair.second_currency_name,
                                                    is_stationarity_second_currency))

    if is_stationarity_first_currency or is_stationarity_second_currency:
        return currency_pair

    return set_z_score(currency_pair, log_path)

    # Алгоритм открытий и закрытий позиций по валютам


def get_stationarity_state_info(name, is_stationarity=False, ):
    state = get_stationarity_state(is_stationarity)
    return 'Пара {0} имеет {1} ряд.'.format(name, state)


def get_stationarity_state(is_stationarity=False):
    stationarity_in_string = "стационарный"
    non_stationarity_in_string = "нестационарный"

    return stationarity_in_string if is_stationarity else non_stationarity_in_string
