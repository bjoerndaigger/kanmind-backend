from django.db.models import Q
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from boards_app.models import Board
from .serializers import BoardSerializer


class BoardListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BoardSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Board.objects.all()

        return Board.objects.filter(Q(owner=user) | Q(members=user))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
