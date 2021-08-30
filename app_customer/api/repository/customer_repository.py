from uuid import UUID

from api.dto.customer_dto import CustomerDto
from api.models.customer import CustomerModel


class CustomerRepository:

    def __init__(self):
        self.objects = CustomerModel.objects

    def get_by_id(self, customer_id: UUID) -> CustomerDto:
        model = self.objects.get(id=customer_id)
        return model.to_dto() if model else None

    def customer_exists(self, email: str, id: UUID=None) -> bool:
        return self.objects.filter(email=email).exclude(id=id).count() > 0

    def customer_id_exists(self, id: UUID) -> bool:
        return self.objects.filter(id=id).count() > 0

    def save(self, dto: CustomerDto) -> CustomerDto:
        db_model = self.objects.filter(id=dto.id).first() or CustomerModel()
        db_model.name = dto.name
        db_model.email = dto.email
        db_model.save()
        return db_model.to_dto()

    def delete(self, customer_id: UUID) -> None:
        self.objects.filter(id=customer_id).delete()

