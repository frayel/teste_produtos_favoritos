import logging
from uuid import UUID

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from api.dto.favorite_dto import FavoriteDto
from api.exceptions.invalid_operation import InvalidOperationException
from api.repository.favorite_repository import FavoriteRepository
from api.service.customer_service import CustomerService
from api.service.product_service import ProductService


class FavoriteService:

    def __init__(self):
        self.favorite_repository = FavoriteRepository()
        self.product_service = ProductService()
        self.customer_service = CustomerService()

    def create(self, favorite_dto: FavoriteDto) -> FavoriteDto:
        if self.customer_service.exists(favorite_dto.customer):
            result = self.product_service.get_by_product_id(favorite_dto.product)
            if result and not result.code:
                if not self.favorite_repository.product_exists(favorite_dto.customer, favorite_dto.product):
                    favorite_dto = self.favorite_repository.save(favorite_dto)
                    logging.info(f"Favorite Item {favorite_dto.id} created!")
                else:
                    logging.error(f"The product {favorite_dto.product} already registered!")
                    raise InvalidOperationException(f"The product {favorite_dto.product} already registered!")
            elif result:
                logging.error(result.error_message)
                raise InvalidOperationException(result.error_message)
        else:
            logging.error(f"The customer {favorite_dto.customer} does not exists!")
            raise InvalidOperationException(f"The customer {favorite_dto.customer} does not exists!")

        return favorite_dto

    def list(self, customer_id: UUID, page_num: int) -> dict:
        favorite_list = self.favorite_repository.list_by_customer_id(customer_id)
        favorite_list = [self.product_service.get_by_product_id(favorite.product) for favorite in favorite_list]
        paginator = Paginator(favorite_list, 10)
        try:
            favorite_list = paginator.page(page_num)
        except PageNotAnInteger:
            favorite_list = paginator.page(1)
        except EmptyPage:
            favorite_list = paginator.page(paginator.num_pages)
        result = {
            "meta": {
                "page_number": page_num,
                "page_size": len(favorite_list)
            },
            "favorites": [f.to_dict() for f in favorite_list]
        }
        return result
