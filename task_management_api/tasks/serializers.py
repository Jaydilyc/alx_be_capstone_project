from rest_framework import serializers
from django.utils import timezone
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = [
            'id',
            'owner',
            'project',
            'title',
            'description',
            'due_date',
            'priority',
            'status',
            'completed_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'owner', 'completed_at', 'created_at', 'updated_at']

    def validate_due_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value