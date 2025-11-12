from django.db import models
from django.contrib.auth.models import User

from boards_app.models import Board

# Create your models here.

STATUS_CHOICES = [
    ('to-do', 'To Do'),
    ('in-progress', 'In Progress'),
    ('review', 'Review'),
    ('done', 'Done'),
]

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]


class Task(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=11, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES)
    assignee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assigned_tasks", null=True, blank=True)
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviewed_tasks", null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
