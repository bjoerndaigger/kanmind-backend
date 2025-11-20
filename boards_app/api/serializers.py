from django.contrib.auth.models import User
from rest_framework import serializers

from boards_app.models import Board
from tasks_app.models import Comments, Task


class BoardSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id',
                  'title',
                  'members',
                  'member_count',
                  'ticket_count',
                  'tasks_to_do_count',
                  'tasks_high_prio_count',
                  'owner_id']
        extra_kwargs = {'members': {'write_only': True}}

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        board_instance = Board.objects.create(**validated_data)
        board_instance.members.set(members_data)
        return board_instance

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(status='high').count()


class BoardMemberSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return obj.first_name


class TaskInBoardSerializer(serializers.ModelSerializer):
    assignee = BoardMemberSerializer(read_only=True)
    reviewer = BoardMemberSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id',
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


class BoardDetailReadSerializer(serializers.ModelSerializer):
    members = BoardMemberSerializer(read_only=True, many=True)
    tasks = TaskInBoardSerializer(read_only=True, many=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id',
                  'members', 'tasks']

    def get_comments_count(self, obj):
        return Comments.objects.filter(task__board=obj).count()


class BoardDetailWriteSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True)
    members_data = BoardMemberSerializer(
        read_only=True, many=True, source='members')
    owner_data = BoardMemberSerializer(read_only=True, source='owner')

    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'owner_data', 'members_data']
