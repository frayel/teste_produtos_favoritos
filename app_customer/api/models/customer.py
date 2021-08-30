import uuid

from django.db import models

from api.dto.customer_dto import CustomerDto


class CustomerModel(models.Model):

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(null=False, max_length=255)
    email = models.CharField(null=False, max_length=255)

    class Meta:
        db_table = "customer"

    def to_dto(self) -> CustomerDto:
        return CustomerDto(
            id=self.id,
            name=self.name,
            email=self.email,
        )