from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    """
    Represents a project board.

    - Each board has a title.
    - An owner who manages the board.
    - Members who can view or contribute to the board.
    """
    title = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='member_boards')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_boards')

    def __str__(self):
        return self.title
