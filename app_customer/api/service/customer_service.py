import logging
from uuid import UUID

from api.dto.customer_dto import CustomerDto
from api.exceptions.invalid_operation import InvalidOperationException
from api.repository.customer_repository import CustomerRepository


class CustomerService:

    def __init__(self):
        self.customer_repository = CustomerRepository()

    def create(self, customer_dto: CustomerDto) -> CustomerDto:
        if not self.customer_repository.customer_exists(customer_dto.email):
            customer_dto = self.customer_repository.save(customer_dto)
            logging.info(f"Customer {customer_dto.email} created!")
        else:
            raise InvalidOperationException(f"The customer {customer_dto.email} already exists!")
        return customer_dto

    def update(self, customer_dto: CustomerDto) -> CustomerDto:
        if customer_dto.id:
            if not self.customer_repository.customer_exists(customer_dto.email, customer_dto.id):
                customer_dto = self.customer_repository.save(customer_dto)
                logging.info(f"Customer {customer_dto.email} updated!")
            else:
                raise InvalidOperationException(f"The customer {customer_dto.email} already exists!")
        else:
            raise InvalidOperationException(f"The customer id must be informed!")
        return customer_dto

    def view(self, customer_id: UUID) -> CustomerDto:
        return self.customer_repository.get_by_id(customer_id)

    def exists(self, customer_id: UUID) -> bool:
        return self.customer_repository.customer_id_exists(customer_id)

    def delete(self, customer_id: UUID) -> None:
        self.customer_repository.delete(customer_id)