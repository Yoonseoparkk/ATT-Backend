from abc import ABC, abstractmethod

class NaverOauthService(ABC):
    @abstractmethod
    def naverLoginAddress(self):
        pass

    @abstractmethod
    def requestAccessToken(self, naverAuthCode):
        pass