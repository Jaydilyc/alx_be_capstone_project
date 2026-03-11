from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsTaskOwner


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaskOwner]

    def get_queryset(self):
        queryset = Task.objects.filter(owner=self.request.user)

        status_param = self.request.query_params.get('status')
        priority_param = self.request.query_params.get('priority')
        project_param = self.request.query_params.get('project')
        due_date_param = self.request.query_params.get('due_date')
        ordering_param = self.request.query_params.get('ordering')

        if status_param:
            queryset = queryset.filter(status=status_param)

        if priority_param:
            queryset = queryset.filter(priority=priority_param)

        if project_param:
            queryset = queryset.filter(project_id=project_param)

        if due_date_param:
            queryset = queryset.filter(due_date__date=due_date_param)

        allowed_ordering = ['due_date', '-due_date', 'priority', '-priority', 'created_at', '-created_at']
        if ordering_param in allowed_ordering:
            queryset = queryset.order_by(ordering_param)

        return queryset

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