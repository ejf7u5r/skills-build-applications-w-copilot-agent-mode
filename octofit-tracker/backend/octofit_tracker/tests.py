from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Team, Activity, Workout, LeaderboardEntry

class UserTests(APITestCase):
    def test_create_user(self):
        url = reverse('user-list')
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# Add similar tests for Team, Activity, Workout, LeaderboardEntry
