from rest_framework import serializers

from boards_app.models import Board


class BoardSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']

    def get_member_count(self, obj):
        return obj.members.count()

    # Placeholder, data not yet available
    def get_ticket_count(self, obj):
        return None

    def get_tasks_to_do_count(self, obj):
        return None

    def get_tasks_high_prio_count(self, obj):
        return None
