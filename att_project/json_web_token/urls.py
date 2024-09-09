from django.urls import path
from json_web_token.controller.user_controller import UserCreate, AuthAPIView, UserListView, ForgotPasswordAPIView, \
    ForgotEmailAPIView, MBTIListView, CheckEmailDuplicateAPIView, CheckNicknameDuplicateAPIView

# json_web_token 앱 내에서 사용할 URL 패턴을 정의
urlpatterns = [
    # 회원가입 URL
    path('register/', UserCreate.as_view(), name='register'),

    # 인증 관련 URL
    path('auth/', AuthAPIView.as_view(), name='auth'),

    # 사용자 목록 조회
    path('users/', UserListView.as_view(), name='user-list'),

    # 비밀번호 찾기와 이메일 찾기
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('forgot-email/', ForgotEmailAPIView.as_view(), name='forgot_email'),

    # DB의 MBTI 정보 불러오기
    path('mbti-options/', MBTIListView.as_view(), name='mbti-options'),

    # 이메일 및 닉네임 중복 체크
    path('check-email/', CheckEmailDuplicateAPIView.as_view(), name='check_email'),
    path('check-nickname/', CheckNicknameDuplicateAPIView.as_view(), name='check_nickname'),
]