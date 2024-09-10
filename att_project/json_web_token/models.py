from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom User Manager Class로 사용자, 관리자를 생성하는 메서드
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)  # 고유값 설정
    nickname = models.CharField(max_length=255, unique=True, blank=True, null=True)  # 고유값 설정
    name = models.CharField(max_length=255, default="Unnamed")

    GENDER_CHOICES = [
        ('M', '남자'),
        ('F', '여자'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')

    MBTI_CHOICES = [
        ('INTJ', 'INTJ'), ('INTP', 'INTP'), ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'),
        ('INFJ', 'INFJ'), ('INFP', 'INFP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'),
        ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'),
        ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('ESTP', 'ESTP'), ('ESFP', 'ESFP'),
    ]
    mbti = models.CharField(max_length=4, choices=MBTI_CHOICES, default='INTJ')

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
        return self.email