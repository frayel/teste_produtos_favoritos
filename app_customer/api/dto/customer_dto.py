import re
from dataclasses import dataclass
from uuid import UUID

from api.exceptions.invalid_data import InvalidDataException


@dataclass
class CustomerDto:

    def __init__(self, id: UUID = None, name: str = None, email: str = None):
        self.id = id
        self.name = name
        self.email = email

    def from_dict(self, dict_value: dict):
        self.id = dict_value["id"] if "id" in dict_value else None
        self.name = dict_value["name"] if "name" in dict_value else None
        self.email = dict_value["email"] if "email" in dict_value else None

        return self

    def validate(self):

        if not self.name:
            raise InvalidDataException("Please inform customer full name")

        if self.email is None:
            raise InvalidDataException("Please inform customer e-mail addresss")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise InvalidDataException("Please inform a valid e-mail addresss")

        return self
