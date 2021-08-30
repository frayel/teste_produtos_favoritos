from uuid import UUID

from django.test import TestCase

from api.dto.customer_dto import CustomerDto
from api.models.customer import CustomerModel
from api.repository.customer_repository import CustomerRepository


class CustomerRepositoryTest(TestCase):

    customer: CustomerModel

    @classmethod
    def setUpTestData(cls):
        cls.customer = CustomerModel(
            id=UUID("9c317dd5-a237-4e34-a059-96e7d2183aa9"),
            name="Felipe Rayel",
            email="felipe.rayel@gmail.com",
        )
        cls.customer.save()
        cls.repository = CustomerRepository()

    def test_get_by_id(self):
        uuid = UUID("9c317dd5-a237-4e34-a059-96e7d2183aa9")
        dto = self.repository.get_by_id(uuid)
        self.assertEqual(dto, self.customer.to_dto())

    def test_exists(self):
        result = self.repository.customer_exists("felipe.rayel@gmail.com")
        self.assertTrue(result)

    def test_save(self):
        dto = CustomerDto(
            name="Teste Teste",
            email="teste@gmail.com",
        )
        saved = self.repository.save(dto)
        self.assertIsNotNone(saved.id)
        self.assertEqual(dto, saved)
