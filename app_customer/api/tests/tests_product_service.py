from unittest.mock import patch
from uuid import UUID

from django.test import TestCase

from api.service.product_service import ProductService


class ServiceProductTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.service = ProductService()

    @patch('api.service.product_service.requests.get')
    def test_get_by_product_id(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda: {
            "reviewScore": 4.4166665,
            "title": "Aparelho de Musculação Academia Particular",
            "price": 799.9,
            "brand": "polimet",
            "id": "79b1c283-00ef-6b22-1c8d-b0721999e2f0",
            "image": "http://challenge-api.luizalabs.com/images/79b1c283-00ef-6b22-1c8d-b0721999e2f0.jpg"
            }
        result = self.service.get_by_product_id(UUID("79b1c283-00ef-6b22-1c8d-b0721999e2f0"))
        self.assertEqual(result.reviewScore, 4.4166665)
