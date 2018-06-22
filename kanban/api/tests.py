from django.test import TestCase
from django.urls import reverse

from api.models import User


class AuthViewTests(TestCase):
    def test_successful_signup(self):
        request_body = {"username": "test", "password": "password"}
        response = self.client.post(reverse("api:signup"), request_body)
        response_body = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response_body["token"])

        user = User.objects.get(username="test")
        self.assertIsNotNone(user)
        self.assertNotEqual(user.password, request_body["password"])
