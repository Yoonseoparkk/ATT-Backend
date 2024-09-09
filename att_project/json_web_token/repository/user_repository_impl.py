from json_web_token.models import User
from json_web_token.repository.user_repository import UserRepository

# UserRepository 인터페이스를 구현하여 사용자 생성 로직을 정의하는 클래스
class UserRepositoryImpl(UserRepository):
    # 새로운 사용자를 생성하는 구체적인 구현 메서드
    # email: 사용자의 이메일 주소
    # password: 사용자의 비밀번호
    # name: 사용자의 이름
    # nickname: 사용자의 닉네임
    # mbti: 사용자의 MBTI 유형
    # gender: 사용자의 성별
    # return: 생성된 사용자 인스턴스
    def create_user(self, email, password, name, nickname, mbti, gender):
        # Django ORM을 사용하여 새로운 사용자 인스턴스를 생성하고 데이터베이스에 저장
        user = User.objects.create_user(
            email=email,
            password=password,
            name=name,
            nickname=nickname,
            mbti=mbti,
            gender=gender
        )

        # 생성된 사용자 인스턴스를 반환
        return user