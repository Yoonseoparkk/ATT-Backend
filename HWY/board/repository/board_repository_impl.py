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
        # models.py가 실질적으로 Django 설정과 연결되어 있음
        # 이 부분에 정의된 게시물 객체가 Board에 해당함
        # 즉 DB에서 Board를 표현하는 테이블을 읽어서 그 전체를 반환하는 작업
        return Board.objects.all().order_by('regDate')

    def create(self, boardData):
        board = Board(**boardData)
        board.save()
        return board

    def findByBoardId(self, boardId):
        return Board.objects.get(boardId=boardId)

    def deleteByBoardId(self, boardId):
        board = Board.objects.get(boardId=boardId)
        board.delete()

    def update(self, board, boardData):
        for key, value in boardData.items():
            print(f"key: {key}, value: {value}")
            setattr(board, key, value)

        board.save()
        return board