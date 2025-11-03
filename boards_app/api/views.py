from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from boards_app.models import Board
from .serializers import BoardSerializer


class BoardViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    queryset = Board.objects.all()
    serializer_class = BoardSerializer
