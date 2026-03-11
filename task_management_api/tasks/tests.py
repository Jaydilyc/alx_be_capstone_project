from django.test import TestCase

# Create your tests here.
from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from projects.models import Project
from .models import Task


class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="StrongPass123"
        )
        self.project = Project.objects.create(
            owner=self.user,
            name="Backend Capstone",
            description="Project description"
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_create_task(self):
        data = {
            "project": self.project.id,
            "title": "Build serializers",
            "description": "Create DRF serializers",
            "due_date": (timezone.now() + timedelta(days=2)).isoformat(),
            "priority": "high",
            "status": "pending"
        }
        response = self.client.post("/api/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().owner, self.user)

    def test_due_date_must_be_in_future(self):
        data = {
            "project": self.project.id,
            "title": "Invalid task",
            "description": "Bad due date",
            "due_date": (timezone.now() - timedelta(days=1)).isoformat(),
            "priority": "high",
            "status": "pending"
        }
        response = self.client.post("/api/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_only_user_tasks(self):
        Task.objects.create(
            owner=self.user,
            project=self.project,
            title="Mine",
            description="My task",
            due_date=timezone.now() + timedelta(days=2),
            priority="medium",
            status="pending"
        )

        other_user = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="StrongPass123"
        )
        other_project = Project.objects.create(
            owner=other_user,
            name="Other project",
            description="Other description"
        )
        Task.objects.create(
            owner=other_user,
            project=other_project,
            title="Not Mine",
            description="Other task",
            due_date=timezone.now() + timedelta(days=2),
            priority="medium",
            status="pending"
        )

        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Mine")