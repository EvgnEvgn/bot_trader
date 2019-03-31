from binance.client import Client
from config import BinanceConfig
from Singleton import Singleton


class BinanceClientSingleton(metaclass=Singleton):

    def __init__(self):
        self.client = Client(BinanceConfig.API_KEY, BinanceConfig.API_SECRET)

    def get_client(self) -> Client:
        return self.client
