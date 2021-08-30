from uuid import UUID

from api.dto.favorite_dto import FavoriteDto
from api.models.favorite import FavoriteModel


class FavoriteRepository:

    def __init__(self):
        self.objects = FavoriteModel.objects

    def list_by_customer_id(self, customer: UUID) -> list:
        models = self.objects.filter(customer=customer).all()
        return [model.to_dto() for model in models] if models else list()

    def product_exists(self, customer: UUID, product: UUID) -> bool:
        return self.objects.filter(customer=customer, product=product).count() > 0

    def save(self, dto: FavoriteDto) -> FavoriteDto:
        db_model = self.objects.filter(id=dto.id).first() or FavoriteModel()
        db_model.customer = dto.customer
        db_model.product = dto.product
        db_model.save()
        return db_model.to_dto()
