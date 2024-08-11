from django.urls import path
from json_web_token.controller.user_controller import UserCreate, AuthAPIView

# json_web_token 앱 내에서 사용할 URL 패턴을 정의
urlpatterns = [
    # 회원가입 URL
    path('register/', UserCreate.as_view(), name='register'),

    # 인증 관련 URL
    path('auth/', AuthAPIView.as_view(), name='auth'),
]