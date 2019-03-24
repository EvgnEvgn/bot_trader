import sys

class CurrencyPair:
    def __init__(self):
        self.first_currency_name = ''
        self.second_currency_name = ''
        self.first_currency_closes = []
        self.second_currency_closes = []
        self.z = []
        self.z_upper_limit = sys.float_info.min
        self.z_lower_limit = sys.float_info.min
        self.is_stationarity = False
        self.first_currency_volume = 0
        self.second_currency_volume = 0

    def set_first_currency_volume(self, volume):
        self.first_currency_volume = float(volume)

    def set_second_currency_volume(self, volume):
        self.second_currency_volume = float(volume)

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
