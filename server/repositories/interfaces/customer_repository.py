from abc import ABC, abstractmethod

from dtos import CustomerCreate
from models.customer import Customer


class CustomerRepository(ABC):

    @abstractmethod
    async def create_customer(self, customer: CustomerCreate) -> Customer:
        """create a new customer"""
        pass

    async def get_by_phone(
        self,
        phone: str,
    ) -> Customer | None:
        pass