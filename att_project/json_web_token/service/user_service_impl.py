# 필요한 라이브러리 및 모듈을 임포트
import jwt as pyjwt  # JWT(Json Web Token)를 다루기 위한 라이브러리
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError  # JWT 관련 예외 처리
from rest_framework_simplejwt.tokens import RefreshToken  # SimpleJWT의 리프레시 토큰 클래스
from rest_framework_simplejwt.exceptions import TokenError  # SimpleJWT의 토큰 예외 처리 클래스
from django.contrib.auth import get_user_model  # 현재 활성화된 사용자 모델을 가져오는 함수
from att_project.settings import SECRET_KEY  # Django 설정에서 SECRET_KEY를 가져옴
from json_web_token.serializer.user_serializer import UserSerializer  # 사용자 직렬화 도구
from json_web_token.service.user_service import UserService  # 추상 서비스 클래스 임포트

# 사용자 등록, 인증, 토큰 관리와 관련된 실제 비즈니스 로직을 처리
class UserServiceImpl(UserService):

    # 회원가입을 등록하는 메서드
    def register_user(self, email, password):
        User = get_user_model()  # 현재 활성화된 사용자 모델을 가져옴
        user = User.objects.create_user(email=email, password=password)  # 새 사용자 생성
        return user  # 생성된 사용자 반환

    # 사용자를 인증하는 메서드
    def authenticate_user(self, email, password):
        User = get_user_model()  # 현재 활성화된 사용자 모델을 가져옵니다.
        user = User.objects.get(email=email)  # 주어진 이메일로 사용자 검색
        if user.check_password(password):  # 비밀번호 확인
            return user  # 인증된 사용자 반환
        return None  # 인증 실패 시 None 반환

    # JWT 토큰을 사용하여 사용자를 가져오는 메서드
    def get_user_from_token(self, token):
        try:
            # 토큰을 디코드하여 사용자 ID를 추출합니다.
            decoded_token = pyjwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")
            User = get_user_model()  # 현재 활성화된 사용자 모델을 가져옴.
            user = User.objects.get(id=user_id)  # 사용자 ID로 사용자 검색
            return UserSerializer(user).data  # 사용자 데이터 반환
        except ExpiredSignatureError:
            raise Exception("Token has expired")  # 토큰이 만료된 경우 예외 발생
        except InvalidTokenError:
            raise Exception("Invalid token")  # 토큰이 유효하지 않은 경우 예외 발생

    # 리프레시 토큰을 사용하여 새로운 액세스 토큰을 생성하는 메서드
    def refresh_token(self, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)  # 리프레시 토큰으로 토큰 객체 생성
            new_tokens = {
                'access': str(refresh.access_token),  # 새로운 액세스 토큰 생성
                'refresh': str(refresh)  # 새로운 리프레시 토큰 생성
            }
            # 토큰에서 사용자 ID를 추출하여 사용자 데이터 검색
            user = get_user_model().objects.get(id=refresh.payload['user_id'])
            user_data = UserSerializer(user).data  # 직렬화된 사용자 데이터 반환
            return new_tokens, user_data  # 새로운 토큰과 사용자 데이터 반환
        except TokenError as e:
            raise Exception(f"Token refresh error: {str(e)}")  # 토큰 갱신 실패 시 예외 발생