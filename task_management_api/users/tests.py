from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationTests(APITestCase):
    def test_user_registration(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass123",
            "password2": "StrongPass123"
        }
        response = self.client.post("/api/register/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, "testuser")

    def test_user_login(self):
        User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPass123"
        )

        data = {
            "username": "testuser",
            "password": "StrongPass123"
        }
        response = self.client.post("/api/token/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_profile_requires_authentication(self):
        response = self.client.get("/api/profile/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)