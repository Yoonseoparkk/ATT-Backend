from board.entity.models import Board
from board.repository.board_repository import BoardRepository


class BoardRepositoryImpl(BoardRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self):
        return Board.objects.all().order_by('regDate')

    def create(self, boardData):
        # title, writer, content 내용을 토대로 Board 객체를 생성
        # 이 객체는 또한 models.py에 의해 구성된 객체로
        # save()를 수행하는 순간 DB에 기록됨
        board = Board(**boardData) # 테이블에 들어가야 하기때문에 request에 담긴 순수데이터만 뽑겠다. [] {} ""
        board.save() # baord => 현재 table 상태입니다.
        return board