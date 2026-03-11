from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        task = self.get_object()

        if task.status == Task.StatusChoices.COMPLETED:
            return Response(
                {"detail": "Task is already completed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        task.status = Task.StatusChoices.COMPLETED
        task.completed_at = timezone.now()
        task.save()

        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def incomplete(self, request, pk=None):
        task = self.get_object()

        if task.status != Task.StatusChoices.COMPLETED:
            return Response(
                {"detail": "Only completed tasks can be marked incomplete."},
                status=status.HTTP_400_BAD_REQUEST
            )

        task.status = Task.StatusChoices.PENDING
        task.completed_at = None
        task.save()

        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)