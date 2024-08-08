from django.db import models


class AccountLoginType(models.Model):
    class LoginType(models.TextChoices):
        GOOGLE = 'GOOGLE', 'Google'
        KAKAO = 'KAKAO', 'Kakao'
        NAVER = 'NAVER', 'Naver'

    loginType = models.CharField(max_length=10, choices=LoginType.choices)

    def __str__(self):
        return self.loginType

    class Meta:
        db_table = 'account_login_type'
        app_label = 'account'