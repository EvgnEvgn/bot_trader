from objects.trade_state_position import TradeStatePosition
from objects.trade_info import TradeInfo


class TradeState:
    def __init__(self):
        self.purchase_info = TradeInfo()
        self.sell_info = TradeInfo()
        self.trade_state_position = TradeStatePosition.CLOSED
