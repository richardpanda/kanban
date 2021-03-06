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

    def test_signup_without_username(self):
        request_body = {"password": "password"}
        response = self.client.post(reverse("api:signup"), request_body)
        response_body = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response_body["errors"]), 1)
        self.assertEqual(response_body["errors"][0]["field"], "username")
        self.assertEqual(
            response_body["errors"][0]["message"], "This field is required."
        )

    def test_signup_without_password(self):
        request_body = {"username": "test"}
        response = self.client.post(reverse("api:signup"), request_body)
        response_body = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response_body["errors"]), 1)
        self.assertEqual(response_body["errors"][0]["field"], "password")
        self.assertEqual(
            response_body["errors"][0]["message"], "This field is required."
        )

    def test_signup_with_registered_username(self):
        username, password = "test", "password"
        user = User.objects.create(username=username, password=password)
        user.save()

        request_body = {"username": username, "password": password}
        response = self.client.post(reverse("api:signup"), request_body)
        response_body = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response_body["errors"]), 1)
        self.assertEqual(response_body["errors"][0]["field"], "username")
        self.assertEqual(
            response_body["errors"][0]["message"],
            "user with this username already exists.",
        )
