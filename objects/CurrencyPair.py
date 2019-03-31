import sys


class CurrencyPair:
    def __init__(self):
        self.first_currency_name = ''
        self.second_currency_name = ''
        self.first_currency_closes = []
        self.second_currency_closes = []
        self.first_currency_market_purchase_price = 0,
        self.first_currency_market_sell_price = 0,
        self.second_currency_market_purchase_price = 0,
        self.second_currency_market_sell_price = 0,
        self.z = []
        self.z_upper_limit = sys.float_info.min
        self.z_lower_limit = sys.float_info.min
        self.is_stationarity = False
        self.first_currency_volume = 0
        self.second_currency_volume = 0
        self.is_first_currency_closes_empty = False
        self.major_currency_name = ''

    def set_first_currency_volume(self, volume):
        self.first_currency_volume = float(volume)

    def set_second_currency_volume(self, volume):
        self.second_currency_volume = float(volume)

    def get_purchase_price_by_currency_name(self, currency_name: str):
        return {
            self.first_currency_name: self.first_currency_market_purchase_price,
            self.second_currency_name: self.second_currency_market_purchase_price,
        }.get(currency_name, 0)

    def get_sell_price_by_currency_name(self, currency_name: str):
        return {
            self.first_currency_name: self.first_currency_market_sell_price,
            self.second_currency_name: self.second_currency_market_sell_price,
        }.get(currency_name, 0)


# def set_second_currency_name(self, second_name):
#     self.second_currency_name = second_name
#
# def set_first_currency_name(self, first_name):
#     self.first_currency_name = first_name
#
# def set_first_currency_closes(self, first_closes):
#     self.first_currency_closes = first_closes
#
# def set_second_currency_closes(self, second_closes):
#     self.second_currency_closes = second_closes
