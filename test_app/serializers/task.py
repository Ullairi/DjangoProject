from rest_framework import serializers
from test_app.models import Task
from test_app.serializers.subtask import SubTaskCreateSerializer
from django.utils import timezone


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline']


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskCreateSerializer(source='subtask_set', many=True, read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'subtasks']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', 'categories']

    def validate_deadline(self, value):
        if value is not None and value < timezone.now():
            raise serializers.ValidationError("Date can't be in past")
        return value
