from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from json_web_token.serializer.user_serializer import UserSerializer
from json_web_token.service.user_service_impl import UserServiceImpl

# API 엔드포인트
class UserCreate(generics.CreateAPIView):
    # UserSerializer를 사용하여 요청 데이터를 직렬화
    serializer_class = UserSerializer
    # UserServiceImpl 인스턴스를 생성하여 사용자 관련 서비스 처리
    user_service = UserServiceImpl()

    # 사용자 생성 시 호출되는 메서드
    def perform_create(self, serializer):
        # user_service를 사용하여 새 사용자 등록
        self.user_service.register_user(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

# 사용자 인증을 처리하는 API 엔드포인트
class AuthAPIView(APIView):
    # UserServiceImpl 인스턴스를 생성하여 인증 관련 서비스 로직을 처리
    user_service = UserServiceImpl()

    # GET 요청을 처리하여 사용자의 로그인 상태를 확인하고, 토큰이 유효하지 않으면 갱신
    def get(self, request):
        try:
            # 쿠키에서 access 토큰을 가져와서 사용자 정보를 조회
            user_data = self.user_service.get_user_from_token(request.COOKIES.get('access'))
            # 사용자 정보를 반환
            return Response(user_data, status=status.HTTP_200_OK)
        except InvalidToken:
            # 토큰이 만료된 경우 refresh 토큰을 사용하여 토큰을 갱신
            refresh_token = request.COOKIES.get('refresh')
            if not refresh_token:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                # 새로운 access, refresh 토큰을 발급
                new_tokens, user_data = self.user_service.refresh_token(refresh_token)
                # 새로운 토큰과 사용자 데이터를 반환
                res = Response(user_data, status=status.HTTP_200_OK)
                # 새로운 토큰을 쿠키에 저장
                res.set_cookie('access', new_tokens['access'], httponly=True)
                res.set_cookie('refresh', new_tokens['refresh'], httponly=True)
                return res
            except TokenError:
                # 토큰 갱신 중 오류가 발생하면 에러 응답을 반환
                return Response(status=status.HTTP_400_BAD_REQUEST)

    # POST 요청을 처리하여 사용자를 인증하고 JWT 토큰을 발급
    def post(self, request):
        # 사용자의 자격 증명을 확인
        user = authenticate(
            email=request.data.get("email"),
            password=request.data.get("password")
        )
        if user is not None:
            # 사용자가 인증되면 UserSerializer로 사용자 데이터를 직렬화
            serializer = UserSerializer(user)
            # JWT 토큰을 생성
            token = TokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
            refresh_token = str(token)
            # 응답에 JWT 토큰과 사용자 데이터를 포함
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # JWT 토큰을 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            # 자격 증명이 유효하지 않은 경우 에러 응답을 반환
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE 요청을 처리하여 사용자를 로그아웃
    def delete(self, request):
        # 응답 객체를 생성하고 로그아웃 성공 메시지 구현
        response = Response({
            "message": "Logout success"
        }, status=status.HTTP_202_ACCEPTED)
        # 쿠키에서 access와 refresh 토큰을 삭제
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response