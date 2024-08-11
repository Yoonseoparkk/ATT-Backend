# 사용자 데이터 액세스 계층을 정의하는 추성 클래스 설정
from abc import ABC, abstractmethod

class UserRepository(ABC):
    # 새로운 사용자를 생성하는 메서드를 정의하는 추상 메서드
        # email: 사용자의 이메일 주소
        # password: 사용자의 비밀번호
        # extra_fields: 추가적인 사용자 정보 (ex. 생년월일, 성별 등)
    @abstractmethod
    def create_user(self, email, password, **extra_fields):
        # 추상 메서드로서, 하위 클래스에서 반드시 구현
        pass