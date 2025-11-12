from django.contrib.auth.models import User
from rest_framework import serializers

from tasks_app.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task

        fields = ['id', 'board', 'title', 'description', 'status',
                  'priority', 'assignee_id', 'reviewer_id', 'due_date']
