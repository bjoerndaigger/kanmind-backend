from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Board(models.Model):
    title = models.CharField(max_length=255)
    members = models.ManyToManyField(User)
