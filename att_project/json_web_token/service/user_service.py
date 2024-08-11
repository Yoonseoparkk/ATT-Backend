from abc import ABC, abstractmethod

class UserService(ABC):
    @abstractmethod
    def register_user(self, email, password, **extra_fields):
        # 회원가입
        pass

    @abstractmethod
    def authenticate_user(self, email, password):
        # 사용자 인증
        pass

    @abstractmethod
    def get_user_from_token(self, token):
        # 사용자의 JWT Token에서 정보 추출
        pass

    @abstractmethod
    def refresh_token(self, refresh_token):
        # JWT Token 재발급
        pass