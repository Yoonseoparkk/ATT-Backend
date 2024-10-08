from django.db import models

class Board(models.Model):
    # 쿼리 대신 이렇게 class type으로 실행시키면 만들어짐
    boardId = models.AutoField(primary_key=True) # AutoField == AutoIncrement 적용
    title = models.CharField(max_length=128, null=False) # 숫자 잘못 입력했을 때 숫자만 바꿔도 알아서 업뎃 됨
    writer = models.CharField(max_length=32, null=False)
    content = models.TextField() # 문자가 긴 경우 TextField 적용
    regDate = models.DateTimeField(auto_now_add=True) # 추가된 현재 시간 적용
    updDate = models.DateTimeField(auto_now=True) # 변경된 현재 시간 적용

    def __str__(self): # 애매함
        return self.title

    class Meta:
        db_table = 'board'
