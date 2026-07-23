from abc import ABC, abstractmethod

from dtos import OrderCreate
from models.order import Order


class OrderRepository(ABC):
    @abstractmethod
    async def create_order(self, order: OrderCreate) -> Order:
        """Persist a new order."""
        pass
