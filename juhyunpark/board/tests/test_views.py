from unittest import TestCase
from unittest.mock import patch, MagicMock

from board.entity.models import Board
from board.service.board_service_impl import BoardServiceImpl

class BoardView(TestCase):

    # 처음 repository를 불러오는 곳에서 mocking을 해야 함!
    # repository는 싱글톤 패턴에 의해 service에서 처음으로 호출되므로 여기에 mocking 해야 함 (중요)
    @patch('board.service.board_service_impl.BoardRepositoryImpl')
    def testList(self, MockBoardRepositoryImpl):
        mockRepository = MockBoardRepositoryImpl.getInstance.return_value
        mockBoardList = [
            Board(boardId=1, title="Test Board 1", content="Content 1"),
            Board(boardId=2, title="Test Board 2", content="Content 2")
        ]
        mockRepository.list.return_value = mockBoardList

        # 이걸 해야 mocking이 제대로 됨
        BoardServiceImpl._BoardServiceImpl__instance = None
        boardService = BoardServiceImpl.getInstance()

        result = boardService.list()

        print(f"result: {result}")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].title, "Test Board 1")
        self.assertEqual(result[1].title, "Test Board 2")

        mockRepository.list.assert_called_once()