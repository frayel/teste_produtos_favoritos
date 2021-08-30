import json
from uuid import UUID

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from api.models.customer import CustomerModel
from api.models.favorite import FavoriteModel


class ApiFavoriteTest(TestCase):

    user: str
    password: str

    @classmethod
    def setUpTestData(cls):
        cls.user = settings.API_USERNAME
        cls.password = settings.API_PASSWORD
        User.objects.create_user(cls.user, "admin@test.com", password=cls.password)
        CustomerModel(id="11111111-1111-1111-1111-111111111111", name="Test", email="test@test.com").save()

    def test_api_add_favorite_ok(self):
        url = reverse("favorite", kwargs={'customer_id': '11111111-1111-1111-1111-111111111111'})
        data = {
            "product": "79b1c283-00ef-6b22-1c8d-b0721999e2f0",
        }
        self.client.login(username=self.user, password=self.password)
        response = self.client.post(url, json.dumps(data), content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FavoriteModel.objects.count(), 1)
        self.assertEqual(FavoriteModel.objects.get().product, UUID("79b1c283-00ef-6b22-1c8d-b0721999e2f0"))
        data = {
            "product": "4bd442b1-4a7d-2475-be97-a7b22a08a024",
        }
        response = self.client.post(url, json.dumps(data), content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FavoriteModel.objects.count(), 2)


    def test_api_add_favorite_without_authentication(self):
        url = reverse("favorite", kwargs={'customer_id': '11111111-1111-1111-1111-111111111111'})
        data = {
            "product": "79b1c283-00ef-6b22-1c8d-b0721999e2f0",
        }
        response = self.client.post(url, json.dumps(data), content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_add_favorite_empty_data(self):
        url = reverse("favorite", kwargs={'customer_id': '11111111-1111-1111-1111-111111111111'})
        data = {
            "product": "",
        }
        self.client.login(username=self.user, password=self.password)
        response = self.client.post(url, json.dumps(data), content_type='text/plain')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_add_favorite_empty_keys(self):
        url = reverse("favorite", kwargs={'customer_id': '11111111-1111-1111-1111-111111111111'})
        data = {}
        self.client.login(username=self.user, password=self.password)
        response = self.client.post(url, json.dumps(data), content_type='text/plain')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_add_favorite_twice(self):
        url = reverse("favorite", kwargs={'customer_id': '11111111-1111-1111-1111-111111111111'})
        data = {
            "product": "79b1c283-00ef-6b22-1c8d-b0721999e2f0",
        }
        self.client.login(username=self.user, password=self.password)
        response = self.client.post(url, json.dumps(data), content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, json.dumps(data), content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_create_user_invalid_product(self):
        url = reverse("favorite", kwargs={'customer_id': '11111111-1111-1111-1111-111111111111'})
        data = {
            "product": "11111111-1111-1111-1111-111111111111",
        }
        self.client.login(username=self.user, password=self.password)
        response = self.client.post(url, json.dumps(data), content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_create_user_invalid_customer(self):
        url = reverse("favorite", kwargs={'customer_id': '11111111-1111-1111-1111-111111111110'})
        data = {
            "product": "79b1c283-00ef-6b22-1c8d-b0721999e2f0",
        }
        self.client.login(username=self.user, password=self.password)
        response = self.client.post(url, json.dumps(data), content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
