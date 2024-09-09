from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from json_web_token.models import User
from json_web_token.serializer.user_serializer import UserSerializer
from json_web_token.service.user_service_impl import UserServiceImpl
from django.core.mail import send_mail
from django.conf import settings

# 회원가입을 처리하는 API 엔드포인트
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
            password=serializer.validated_data['password'],
            name=serializer.validated_data['name'],
            nickname=serializer.validated_data['nickname'],
            mbti=serializer.validated_data['mbti'],
            gender=serializer.validated_data['gender']
        )

# 사용자 인증 및 JWT 토큰을 발급하는 API 엔드포인트
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

# 비밀번호 찾기를 처리하는 API
class ForgotPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            # 비밀번호 재설정 링크 생성 로직
            reset_link = f"{settings.FRONTEND_URL}/reset-password?token={user.id}"

            # 이메일 전송
            send_mail(
                '비밀번호 재설정',
                f'비밀번호를 재설정하려면 다음 링크를 클릭하세요: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response({"message": "비밀번호 재설정 링크가 이메일로 발송되었습니다."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "해당 이메일을 사용하는 계정이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


# 이메일 찾기를 처리하는 API
class ForgotEmailAPIView(APIView):
    def post(self, request):
        name = request.data.get('name')
        nickname = request.data.get('nickname')
        try:
            user = User.objects.get(name=name, nickname=nickname)
            return Response({"email": user.email}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "입력한 정보와 일치하는 계정이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

# 모든 사용자 목록을 가져오는 API
class UserListView(generics.ListAPIView):
    # 모든 사용자 조회
    queryset = User.objects.all()
    # 조회된 사용자를 UserSerializer를 통해 직렬화
    serializer_class = UserSerializer

class MBTIListView(APIView):
    def get(self, request):
        mbti_options = [
            'INTJ', 'INTP', 'ENTJ', 'ENTP',
            'INFJ', 'INFP', 'ENFJ', 'ENFP',
            'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ',
            'ISTP', 'ISFP', 'ESTP', 'ESFP'
        ]
        return Response({"mbti_options": mbti_options}, status=status.HTTP_200_OK)

# 이메일 중복 확인을 위한 API
class CheckEmailDuplicateAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({'is_duplicate': True}, status=status.HTTP_200_OK)
        return Response({'is_duplicate': False}, status=status.HTTP_200_OK)

# 닉네임 중복 확인을 위한 API
class CheckNicknameDuplicateAPIView(APIView):
    def post(self, request):
        nickname = request.data.get('nickname')
        if User.objects.filter(nickname=nickname).exists():
            return Response({'is_duplicate': True}, status=status.HTTP_200_OK)
        return Response({'is_duplicate': False}, status=status.HTTP_200_OK)

# 관리자 회원 관리를 위한 조회
class ManagerView(generics.ListAPIView):
    """
    관리자 뷰: 사용자 목록 조회 및 사용자 관리
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        """
        모든 사용자 목록을 조회합니다.
        """
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        사용자 정보를 기반으로 새로운 사용자 생성 또는 기타 작업을 수행합니다.
        """
        user_data = request.data
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)