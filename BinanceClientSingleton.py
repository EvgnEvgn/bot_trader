from binance.client import Client
from config import BinanceConfig


class BinanceClientSingleton:
    __instance = None

    @staticmethod
    def get_instance():

        if BinanceClientSingleton.__instance is None:
            BinanceClientSingleton()
        return BinanceClientSingleton.__instance

    def __init__(self):

        if BinanceClientSingleton.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.client = Client(BinanceConfig.API_KEY, BinanceConfig.API_SECRET)
            BinanceClientSingleton.__instance = self

    def get_client(self)->Client:
        return self.client
