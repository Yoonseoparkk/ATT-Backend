from abc import ABC, abstractmethod

class RedisService(ABC):
    @abstractmethod
    def storeAccessToken(self, account_id, userToken):
        pass

    @abstractmethod
    def getValueByKey(self, key):
        pass