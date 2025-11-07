from rest_framework import serializers

from boards_app.models import Board


class BoardSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'member_count', 'ticket_count',
                  'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']
        extra_kwargs = {'members': {'write_only': True}}

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        board_instance = Board.objects.create(**validated_data)
        board_instance.members.set(members_data)
        return board_instance

    def get_member_count(self, obj):
        return obj.members.count()

    # Placeholder, data not yet available
    def get_ticket_count(self, obj):
        return None

    def get_tasks_to_do_count(self, obj):
        return None

    def get_tasks_high_prio_count(self, obj):
        return None


class BoardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'
