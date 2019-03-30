class CurrencyAccount:
    def __init__(self, currency: str, amount: float):
        self.currency = currency
        self.amount = amount


class Wallet:
    def __init__(self):
        self.currency_accounts = {}

    def add_currency_account(self, currency: str, amount: float):
        self.currency_accounts[currency] = amount

