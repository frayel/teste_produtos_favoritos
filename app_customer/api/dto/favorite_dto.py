from dataclasses import dataclass
from uuid import UUID

from api.exceptions.invalid_data import InvalidDataException


@dataclass
class FavoriteDto:

    def __init__(self, id: UUID = None, customer: UUID = None, product: UUID = None):
        self.id = id
        self.customer = customer
        self.product = product

    def from_dict(self, dict_value: dict):
        self.id = dict_value["id"] if "id" in dict_value else None
        self.customer = dict_value["customer"] if "customer" in dict_value else None
        self.product = dict_value["product"] if "product" in dict_value else None

        return self

    def validate(self):

        if self.product is None:
            raise InvalidDataException("Please inform product id")

        return self