from django.contrib.auth.models import User

from rest_framework import serializers

from boards_app.api.serializers import BoardMemberSerializer
from tasks_app.models import Task, Comments


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
                  'comments_count'
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)

        if request and request.method == 'PATCH':
            self.fields.pop('board', None)
            self.fields.pop('comments_count', None)

    def get_comments_count(self, obj):
        return Comments.objects.filter(task=obj).count()


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
        return Comments.objects.filter(task=obj).count()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.first_name')
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'created_at', 'author', 'content']
      
