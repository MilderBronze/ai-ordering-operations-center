from abc import ABC, abstractmethod

from dtos import CustomerCreate
from models.customer import Customer


class CustomerRepository(ABC):

    @abstractmethod
    async def create_customer(self, customer: CustomerCreate) -> Customer:
        """create a new customer"""
        pass