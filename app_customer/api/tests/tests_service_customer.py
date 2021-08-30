from django.test import TestCase

from api.dto.customer_dto import CustomerDto
from api.service.customer_service import CustomerService


class ServiceCustomerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.service = CustomerService()

    def test_customer_service(self):
        dto = CustomerDto(name="Test", email="teste@teste.com")
        customer = self.service.create(dto)
        self.assertEqual(customer.name, dto.name)
        dto.name = "Other Name"
        dto.id = customer.id
        customer = self.service.update(dto)
        self.assertEqual(customer.name, dto.name)
        customer = self.service.view(customer.id)
        self.assertEqual(customer.name, dto.name)
        self.service.delete(customer.id)
