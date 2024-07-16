from django.db import models

# Create your models here.
class Board(models.Model):
    BoardId = models.AutoField(primary_key=True)
    BoardName = models.CharField(max_length=32)
    BoardContext = models.TextField()
    BoardWriter = models.CharField(max_length=32)
    regDate = models.DateTimeField(auto_now_add=True)
    updDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"BoardId: {self.BoardId}, boardName: {self.BoardName}"
    # Board 객체를 출력하고자 하면, 위에 처럼 나왔으면 좋겠다.

    # 이름이 원하는대로 안나와.( 현석이 경험당)
    class Meta:
        db_table = "board"
