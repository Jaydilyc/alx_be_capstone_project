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

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)

        if instance and instance.status == Task.StatusChoices.COMPLETED:
            incoming_status = attrs.get('status', instance.status)

            editable_fields = ['title', 'description', 'due_date', 'priority', 'project']
            tried_to_edit_protected_field = any(field in attrs for field in editable_fields)

            if incoming_status == Task.StatusChoices.COMPLETED and tried_to_edit_protected_field:
                raise serializers.ValidationError(
                    "Completed tasks cannot be edited unless marked incomplete first."
                )

        return attrs