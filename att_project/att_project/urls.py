"""
URL configuration for att_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# 설정에 필요한 모듈들을 임포트합니다.
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView  # JWT 토큰 갱신

# URL 패턴을 정의하는 리스트
urlpatterns = [
    # Django 관리자 사이트에 대한 URL
    path("admin/", admin.site.urls),

    # 'board' 앱의 URL 설정
    path('board/', include('board.urls')),

    # 'account' 앱의 URL 설정
    path('account/', include('account.urls')),

    # Google OAuth 인증과 관련된 URL 설정
    path('google_oauth/', include('google_oauth.urls')),

    # Kakao OAuth 인증과 관련된 URL 설정
    path('kakao_oauth/', include('kakao_oauth.urls')),

    # Naver OAuth 인증과 관련된 URL 설정
    path('naver_oauth/', include('naver_oauth.urls')),

    # Redis 관련된 URL 설정
    path('redis_token/', include('redis_token.urls')),

    # JWT 관련 URL
    path('api/', include('json_web_token.urls')),

    # JWT 토큰을 갱신하는 URL
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]