from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from board.entity.models import Board
from board.serializers import BoardSerializer
from board.service.board_service_impl import boardServiceImpl


# Create your views here.
class BoardView(viewsets.ViewSet):
    queryset = Board.objects.all()
    boardService = boardServiceImpl.getInstance()

    def list(self,request):
        boardList = self.boardService.list()
        serializer = BoardSerializer(boardList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
