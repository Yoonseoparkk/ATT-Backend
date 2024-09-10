from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from board.entity.models import Board
from board.serializers import BoardSerializer
from board.service.board_service_impl import BoardServiceImpl


# viewsets를 사용하려면 rest_framework가 설치되어야 합니다.
# pip install dgangorestframework
class BoardView(viewsets.ViewSet): # viewset 왜 사용하는지 알아보기 >> CRUD에 있어서 코드관리와 편의성이 위주인 것 같음
    queryset = Board.objects.all() # 이렇게 선언해줘야 Board Entity가 db처럼 사용가능 (중요)
    # entity class가 save, delete를 사용할 수있고, id 입력주면 관련된 데이터들을 get할 수 있도록 해줌

    boardService = BoardServiceImpl.getInstance() # 외부 요청을 service로 보내기 위함
    # 1단계 하단에 보내기 위해서 징검다리(통로)가 필요한데 이 통로 역할을 getInstance()가 해줍니다.

    # 인증된 사용자만 접근 가능
    permission_classes = [IsAuthenticated]

    def list(self, request): # controller는 외부요청(vue 요청)을 다루기 때문에 함수 입력 인자로 request 포함됩니다.
        boardList = self.boardService.list()
        serializer = BoardSerializer(boardList, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            board = self.boardService.createBoard(serializer.validated_data)
            return Response(BoardSerializer(board).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)