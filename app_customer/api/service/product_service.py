import logging
from uuid import UUID

import requests
from django.conf import settings
from django.core.cache import cache

from api.dto.product_dto import ProductDto
from api.repository.favorite_repository import FavoriteRepository


class ProductService:

    def __init__(self):
        self.favorite_repository = FavoriteRepository()

    def get_by_product_id(self, product_id: UUID) -> ProductDto:
        product = cache.get(f"product_{product_id}")
        if not product:
            url = settings.PRODUCT_ENDPOINT.replace("<ID>", str(product_id))
            response = requests.get(url, timeout=10)
            product = ProductDto().from_dict(response.json())
            cache.set(f"product_{product_id}", product, 300)  # Mantem cache da consulta por 5 min
        logging.info(f"Product {product_id} found.")
        return product
