from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from django.conf import settings


@dataclass
class ProductDto:

    def __init__(self, id: UUID = None, price: Decimal = None, image: str = None, brand: str = None, title: str = None,
                 reviewScore: Decimal = None, code: str = None, error_message: str = None):
        self.id = id
        self.price = price
        self.image = image
        self.brand = brand
        self.title = title
        self.reviewScore = reviewScore
        self.code = code
        self.error_message = error_message

    def to_dict(self):
        data = self.__dict__
        data["link"] = settings.PRODUCT_ENDPOINT.replace("<ID>", self.id)
        if not self.code:
            del data["code"]
            del data["error_message"]
        if not self.reviewScore:
            del data["reviewScore"]
        return data

    def from_dict(self, dict_value: dict):
        self.id = dict_value["id"] if "id" in dict_value else None
        self.price = dict_value["price"] if "price" in dict_value else None
        self.image = dict_value["image"] if "image" in dict_value else None
        self.brand = dict_value["brand"] if "brand" in dict_value else None
        self.title = dict_value["title"] if "title" in dict_value else None
        self.reviewScore = dict_value["reviewScore"] if "reviewScore" in dict_value else None
        self.code = dict_value["code"] if "code" in dict_value else None
        self.error_message = dict_value["error_message"] if "error_message" in dict_value else None

        return self
