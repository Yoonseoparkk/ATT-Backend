from att_project import settings
import redis_token

from redis_token.service.redis_service import RedisService


class RedisServiceImpl(RedisService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.redis_client = redis_token.StrictRedis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                decode_responses=True
            )

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def storeAccessToken(self, account_id, userToken):
        try:
            self.redis_client.set(userToken, account_id)
        except Exception as e:
            print('Error storing access token in Redis:', e)
            raise e

    def getValueByKey(self, key):
        try:
            return self.redis_client.get(key)
        except Exception as e:
            print("redis_token key로 value 찾는 중 에러 발생:", e)
            raise e
