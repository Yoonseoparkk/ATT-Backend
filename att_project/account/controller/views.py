from rest_framework import viewsets, status
from rest_framework.response import Response

from account.repository.profile_repository_impl import ProfileRepositoryImpl
from account.serializers import AccountSerializer
from account.service.account_service_impl import AccountServiceImpl
from redis_token.service.redis_service_impl import RedisServiceImpl


class AccountView(viewsets.ViewSet):
    accountService = AccountServiceImpl.getInstance()
    redisService = RedisServiceImpl.getInstance()
    profileRepository = ProfileRepositoryImpl.getInstance()

    def checkEmailDuplication(self, request):
        print("checkEmailDuplication()")

        try:
            email = request.data.get('email')
            isDuplicate = self.accountService.checkEmailDuplication(email)

            return Response({'isDuplicate': isDuplicate, 'message': 'Email이 이미 존재합니다.' \
                if isDuplicate else '사용 가능한 email 입니다.'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("이메일 중복 체크 중 에러 발생:", e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def checkNicknameDuplication(self, request):
        print("checkNicknameDuplication()")

        try:
            nickname = request.data.get('newNickname')
            print(f"nickname: {nickname}")
            isDuplicate = self.accountService.checkNicknameDuplication(nickname)

            return Response({'isDuplicate': isDuplicate, 'message': 'Nickname이 이미 존재합니다.' \
                if isDuplicate else '사용 가능한 nickname 입니다.'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("닉네임 중복 체크 중 에러 발생:", e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def registerAccount(self, request):
        try:
            loginType = request.data.get('loginType')
            nickname = request.data.get('nickname')
            email = request.data.get('email')

            account = self.accountService.registerAccount(
                loginType=loginType,
                roleType='NORMAL',
                nickname=nickname,
                email=email,
            )

            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("계정 생성 중 에러 발생:", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def getNickname(self, request):
        userToken = request.data.get("userToken")
        if not userToken:
            return Response(None, status=status.HTTP_200_OK)
        accountId = self.redisService.getValueByKey(userToken)
        profile = self.profileRepository.findById(accountId)
        if profile is None:
            return Response(
                {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        nickname = profile.nickname
        return Response(nickname, status=status.HTTP_200_OK)

    def getEmail(self, request):
        userToken = request.data.get("userToken")
        if not userToken:
            return Response(None, status=status.HTTP_200_OK)
        accountId = self.redisService.getValueByKey(userToken)
        profile = self.profileRepository.findById(accountId)
        if profile is None:
            return Response(
                {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        email = profile.email
        return Response(email, status=status.HTTP_200_OK)


