import uuid

from django.db import models

from api.dto.favorite_dto import FavoriteDto


class FavoriteModel(models.Model):

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    customer = models.UUIDField(null=False)
    product = models.UUIDField(null=False)

    class Meta:
        db_table = "favorite"

    def to_dto(self) -> FavoriteDto:
        return FavoriteDto(
            id=self.id,
            customer=self.customer,
            product=self.product,
        )