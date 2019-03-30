from wallet import Wallet
from CurrencyPair import CurrencyPair
from trade_state_position import TradeStatePosition
from config import BinanceConfig
from trade_state import TradeState


class TradeManagerStub:
    def __init__(self, wallet: Wallet):
        self.wallet = wallet

    def purchase(self, purchase_currency: str, sell_currency: str, count, price_bid: float, commission: float,
                 trade_state: TradeState):
        purchase_currency_amount = self.wallet.currency_accounts[purchase_currency]
        sell_currency_amount = self.wallet.currency_accounts[sell_currency]

        if purchase_currency_amount is None or sell_currency_amount is None:
            print('Ошибка нет переданых валют в кошельке')
            return False

        total_purchase_currency_count = price_bid * count

        if sell_currency_amount < total_purchase_currency_count:
            print('Недосточно средств')
            return False

        self.wallet.currency_accounts[sell_currency] -= total_purchase_currency_count
        self.wallet.currency_accounts[purchase_currency] += count * (1 - commission)

        trade_state.purchase_info.purchase_currency = purchase_currency
        trade_state.purchase_info.sell_currency = sell_currency
        trade_state.purchase_info.count = count * (1 - commission)
        trade_state.purchase_info.total_price = total_purchase_currency_count

        return True

    def sell(self, purchase_currency: str, sell_currency: str, count, price_ask: float, commission: float,
             trade_state: TradeState):
        purchase_currency_amount = self.wallet.currency_accounts[purchase_currency]
        sell_currency_amount = self.wallet.currency_accounts[sell_currency]

        if purchase_currency_amount is None or sell_currency_amount is None:
            print('Ошибка нет переданых валют в кошельке')
            return False

        total_sell_price = price_ask * count * (1 - commission)

        if sell_currency_amount < count:
            print('Недосточно средств')
            return False

        self.wallet.currency_accounts[sell_currency] -= count
        self.wallet.currency_accounts[purchase_currency] += total_sell_price

        trade_state.sell_info.purchase_currency = purchase_currency
        trade_state.sell_info.sell_currency = sell_currency
        trade_state.sell_info.count = count
        trade_state.sell_info.total_price = total_sell_price
        return True

    def open_high_position(self, currency_pair: CurrencyPair,
                           count_purchase: float, count_sell: float,
                           commission, trade_state: TradeState):

        if trade_state.trade_state_position == TradeStatePosition.CLOSED:
            purchase_result = self.purchase(currency_pair.first_currency_name,
                                            currency_pair.major_currency_name, count_purchase,
                                            currency_pair.first_currency_market_purchase_price,
                                            commission, trade_state)

            sell_result = self.sell(currency_pair.second_currency_name,
                                    currency_pair.major_currency_name, count_sell,
                                    currency_pair.second_currency_market_sell_price, commission, trade_state)
            if purchase_result and sell_result:
                trade_state.trade_state_position = TradeStatePosition.HIGH_OPENED

    def open_low_position(self, currency_pair: CurrencyPair,
                          count_purchase: float, count_sell: float,
                          commission, trade_state: TradeState):

        if trade_state.trade_state_position == TradeStatePosition.CLOSED:
            purchase_result = self.purchase(currency_pair.second_currency_name,
                                            currency_pair.major_currency_name, count_purchase,
                                            currency_pair.second_currency_market_purchase_price,
                                            commission, trade_state)

            sell_result = self.sell(currency_pair.first_currency_name,
                                    currency_pair.major_currency_name, count_sell,
                                    currency_pair.first_currency_market_sell_price,
                                    commission, trade_state)

            if purchase_result and sell_result:
                trade_state.trade_state_position = TradeStatePosition.LOW_OPENED

    def close_position(self, currency_pair: CurrencyPair, trade_state: TradeState):
        if trade_state.trade_state_position == TradeStatePosition.CLOSED:
            print('Не может быть выполнено в данном состоянии')
            return False

        commission = BinanceConfig.COMMISSION

        sell_info_purchase_currency = trade_state.purchase_info.sell_currency
        sell_info_sell_currency = trade_state.purchase_info.purchase_currency
        sell_info_count = trade_state.purchase_info.count
        sell_info_price = currency_pair.get_sell_price_by_currency_name(sell_info_purchase_currency)
        if sell_info_price == 0:
            return print('Цена не моэет быть равна 0!!!')

        purchase_info_purchase_currency = trade_state.sell_info.sell_currency
        purchase_info_sell_currency = trade_state.sell_info.purchase_currency
        purchase_info_count = trade_state.sell_info.total_price
        purchase_info_price = currency_pair.get_purchase_price_by_currency_name(purchase_info_sell_currency)
        if purchase_info_price == 0:
            return print('Цена не моэет быть равна 0!!!')

        result_sell = self.sell(sell_info_purchase_currency,
                                sell_info_sell_currency,
                                sell_info_count,
                                sell_info_price,
                                commission,
                                trade_state)

        result_purchase = self.purchase(purchase_info_purchase_currency,
                                        purchase_info_sell_currency,
                                        purchase_info_count,
                                        purchase_info_price,
                                        commission,
                                        trade_state)

        if result_sell and result_purchase:
            trade_state.trade_state_position = TradeStatePosition.CLOSED
