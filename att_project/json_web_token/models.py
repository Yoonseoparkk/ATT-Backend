from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom User Manager Class로 사용자를 생성하고 관리자를 생성하는 메서드 입니다.
class UserManager(BaseUserManager):
    # 주어진 이메일과 비밀번호를 일반 사용자 인스턴스로 생성합니다.
    # 각각의 매게변수 설명
    # email: 사용자의 이메일 주소
    # password: 사용자의 비밀번호
    # extra_field: 기본적인 이메일 주소, 비밀번호만 설정 했지만 나중에, MBTI, 나이, 생년월일을 설정할 수 있음
    # return: 생성된 사용자 인스턴스
    # raises ValueError: 이메일 (필수값)이 없으면 발생하는 에러 설정
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            # 이메일 필드는 필수로 제공되는 에러 문구 설정
            raise ValueError('The Email field must be set')

        # 이메일 주소를 정규화하여 저장
        email = self.normalize_email(email)
        # 사용자 모델의 인스턴스 생성
        user = self.model(email=email, **extra_fields)
        # 비밀번호를 Hash화하여 설정
        user.set_password(password)
        # Database에 사용자 저장
        user.save(using=self._db)

        return user

    # 주어진 이메일과 비밀번호로 관리자 인스턴스를 생성합니다.
    # 각각의 매게변수 설명
    # email, password, extra_fields, return 위와 동일
    def create_superuser(self, email, password=None, **extra_fields):
        # 관리자 권한을 설정하기 위한 필드 기본값 설정
        # 슈퍼유저 권한 부여
        extra_fields.setdefault('is_superuser', True)
        # 관리자 사이트 접근 권한 부여
        extra_fields.setdefault('is_staff', True)
        # 사용자 활성화 상태 설정
        extra_fields.setdefault('is_active', True)
        # 일반 사용자 생성 메서드를 호출하여 슈퍼유저를 생성.
        return self.create_user(email, password, **extra_fields)

# Custom User Model로 Django의 기본 사용자 Model을 Custom해 이메일로 로그인 및 권한을 관리
class User(AbstractBaseUser, PermissionsMixin):
    # 사용자 이메일 주소를 정의하고 최대 255자까지 허용
    email = models.EmailField(max_length=255, unique=True)

    # 사용자의 활성화 상태로 기본값은 활성화(True)임
    is_active = models.BooleanField(default=True)

    # 관리 사이트 접근 권한으로 기본값은 비활성화(False)임
    is_staff = models.BooleanField(default=False)

    # 관리자의 권한으로 기본값을 비활성화(Fasle)임
    is_superuser = models.BooleanField(default=False)

    # 사용자가 생성된 날짜와 시간 (자동으로 생성되게 설정)
    created_at = models.DateTimeField(auto_now_add=True)

    # 사용자가 마지막으로 수정한 날짜와 시간 (자동으로 업데이트되게 설정)
    updated_at = models.DateTimeField(auto_now=True)

    # 사용자 모델에서 사용자는 매니저 인스턴스
    objects = UserManager()

    # 로그인 시 사용할 필드로 email로 설정함
    USERNAME_FIELD = 'email'

    # 필수 입력 필드로 현재는 email 외에는 입력된 필드가 없다.
    REQUIRED_FIELDS = []

    # 사용자 인스턴스를 문자열로 표현해 이메일 주소를 반환한다.
    def __str__(self):
        # 사용자 이메일 주소 반환
        return self.email