from board.repository.board_repository_impl import BoardRepositoryImpl
from board.service.board_service import BoardService


class boardServiceImpl(BoardService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__boardRepository = BoardRepositoryImpl.getInstance()

        return cls.__instance
    # 클래스매서드를 써줘야 cls를 쓸 수 있다. 아니면 self를 써야지
    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self):
        return self.__boardRepository.list()
