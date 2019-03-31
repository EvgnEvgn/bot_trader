import redis
from config import RedisConfig
from objects.Singleton import Singleton


class RedisClientSingleton(metaclass=Singleton):
    __instance = None

    def __init__(self):
        self.client = redis.Redis(host=RedisConfig.HOST, port=RedisConfig.PORT, db=RedisConfig.DB)
        RedisClientSingleton.__instance = self

    def get_client(self) -> redis.Redis:
        return self.client
