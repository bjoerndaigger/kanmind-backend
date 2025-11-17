from django.contrib.auth.models import User

from rest_framework import serializers

from boards_app.api.serializers import BoardMemberSerializer
from tasks_app.models import Task


class TaskSerializer(serializers.ModelSerializer):
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='assignee')
    assignee = BoardMemberSerializer(read_only=True)

    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='reviewer')
    reviewer = BoardMemberSerializer(read_only=True)

    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task

        fields = ['id',
                  'board',
                  'title',
                  'description',
                  'status',
                  'priority',
                  'assignee', 'assignee_id',
                  'reviewer', 'reviewer_id',
                  'due_date',
                  'comments_count']

    def get_comments_count(self, obj):
        # Placeholder, data not yet available
        return 0


class TaskReadSerializer(serializers.ModelSerializer):
    assignee = BoardMemberSerializer(read_only=True)
    reviewer = BoardMemberSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id',
                  'board',
                  'title',
                  'description',
                  'status',
                  'priority',
                  'assignee',
                  'reviewer',
                  'due_date',
                  'comments_count']

    def get_comments_count(self, obj):
        # Placeholder, data not yet available
        return 0
