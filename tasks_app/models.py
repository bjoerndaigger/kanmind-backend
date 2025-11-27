from django.db import models
from django.contrib.auth.models import User

from boards_app.models import Board


# Task status options
STATUS_CHOICES = [
    ('to-do', 'To Do'),
    ('in-progress', 'In Progress'),
    ('review', 'Review'),
    ('done', 'Done'),
]

# Task priority options
PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]


class Task(models.Model):
    """
    Represents a task within a board.

    - Each task belongs to a board.
    - Has an assignee and optionally a reviewer.
    - Tracks status, priority, and due date.
    """
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=11, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewed_tasks', null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)


class Comments(models.Model):
    """
    Represents a comment on a task.

    - Each comment is authored by a user.
    - Linked to a specific task.
    - Creation timestamp is auto-generated.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_comments')
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
