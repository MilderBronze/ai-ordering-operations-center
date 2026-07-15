from abc import ABC, abstractmethod

from models.customer import Customer


class CustomerRepository(ABC):

    @abstractmethod
    def create_customer(self) -> Customer:
        """create a new customer"""
        pass