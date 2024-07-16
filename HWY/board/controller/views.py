from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from board.entity.models import Board
from board.serializers import BoardSerializer
from board.service.board_service_impl import BoardServiceImpl

class BoardView(viewsets.ViewSet):
    queryset = Board.objects.all()
    boardService = BoardServiceImpl.getInstance()

    def list(self, request):
        boardList = self.boardService.list()
        print('boardList:', boardList)
        serializer = BoardSerializer(boardList, many=True)
        print('serialized boardList:', serializer.data)
        return Response(serializer.data)

    def create(self, request):
        serializer = BoardSerializer(data=request.data)

        if serializer.is_valid():
            board = self.boardService.createBoard(serializer.validated_data)
            return Response(BoardSerializer(board).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def read(self, request, pk=None):
        board = self.boardService.readBoard(pk)
        serializer = BoardSerializer(board)
        return Response(serializer.data)

    def removeBoard(self, request, pk=None):
        self.boardService.removeBoard(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def modifyBoard(self, request, pk=None):
        board = self.boardService.readBoard(pk)
        serializer = BoardSerializer(board, data=request.data, partial=True)

        if serializer.is_valid():
            updatedBoard = self.boardService.updateBoard(pk, serializer.validated_data)
            return Response(BoardSerializer(updatedBoard).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)