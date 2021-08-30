import json
from uuid import UUID

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from api.models.customer import CustomerModel


class ApiCustomerTest(TestCase):

    user: str
    password: str

    @classmethod
    def setUpTestData(cls):
        cls.user = settings.API_USERNAME
        cls.password = settings.API_PASSWORD
        User.objects.create_user(cls.user, "admin@test.com", password=cls.password)

    def test_api_create_user_ok(self):
        url = reverse("customer")
        data = {
            "name": "Felipe Rayel",
            "email": "felipe.rayel@gmail.com"
        }
        self.client.login(username=self.user, password=self.password)
        response = self.client.post(url, json.dumps(data), content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomerModel.objects.count(), 1)
        self.assertEqual(CustomerModel.objects.get().email, "felipe.rayel@gmail.com")

    def test_api_create_user_without_authentication(self):
        url = reverse("customer")
        data = {
            "name": "Felipe Rayel",
            "email": "felipe.rayel@gmail.com"
        }
        response = self.client.post(url, json.dumps(data), content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_customer_empty_data(self):
        url = reverse("customer")
        data = {
            "name": "",
            "email": ""
        }
        self.client.login(username=self.user, password=self.password)
        response = self.client.post(url, json.dumps(data), content_type='text/plain')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_customer_empty_keys(self):
        url = reverse("customer")
        data = {}
        self.client.login(username=self.user, password=self.password)
        response = self.client.post(url, json.dumps(data), content_type='text/plain')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_customer_twice(self):
        url = reverse("customer")
        data = {
            "name": "Felipe Rayel",
            "email": "felipe.rayel@gmail.com"
        }
        self.client.login(username=self.user, password=self.password)
        response = self.client.post(url, json.dumps(data), content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, json.dumps(data), content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_create_user_invalid_email(self):
        url = reverse("customer")
        data = {
            "name": "Felipe Rayel",
            "email": "xxxxxxxxxxx"
        }
        self.client.login(username=self.user, password=self.password)
        response = self.client.post(url, json.dumps(data), content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
