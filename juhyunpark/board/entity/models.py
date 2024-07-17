from django.db import models

# Create your models here.
class Board(models.Model):
    boardId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, null=False)
    writer = models.CharField(max_length=32, null=False)
    content = models.TextField()
    regDate = models.DateTimeField(auto_now_add=True)
    updDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"BoardId: {self.boardId}, boardName: {self.title}"
    # Board 객체를 출력하고자 하면, 위에 처럼 나왔으면 좋겠다.

    # 이름이 원하는대로 안나와.( 현석이 경험당)
    class Meta:
        db_table = "board"
