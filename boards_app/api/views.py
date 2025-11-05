from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from boards_app.models import Board
from .serializers import BoardSerializer


class BoardViewSet(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
