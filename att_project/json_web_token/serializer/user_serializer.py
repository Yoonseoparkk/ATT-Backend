from rest_framework import serializers
from json_web_token.models import User

# User Serializer 클래스 정의
class UserSerializer(serializers.ModelSerializer):
    # password 필드를 write-only로 설정하여 응답에 포함되지 않도록 처리
    password = serializers.CharField(write_only=True)

    # Meta 클래스에서 Serializer의 설정을 정의
    class Meta:
        # 직렬화/역직렬화할 모델을 User로 설정
        model = User
        # 포함할 필드를 명시 (email, password, name, nickname, mbti, gender, created_at, updated_at)
        fields = ('email', 'password', 'name', 'nickname', 'mbti', 'gender', 'created_at', 'updated_at')
        # 추가적인 필드 옵션을 설정
        extra_kwargs = {
            # password 필드를 write-only로 설정하여 사용자에게 노출되지 않게 함
            'password': {'write_only': True}
        }

    # 새로운 사용자 인스턴스를 생성하는 메서드
    def create(self, validated_data):
        # 비밀번호를 해시화하여 저장하고, 추가된 필드(name, nickname, mbti, gender)를 처리
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            nickname=validated_data['nickname'],
            mbti=validated_data['mbti'],
            gender=validated_data['gender']
        )
        # 생성된 사용자 인스턴스를 반환
        return user