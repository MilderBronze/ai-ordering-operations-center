from abc import ABC, abstractmethod

from dtos import OrderItemCreate
from models.order_item import OrderItem


class OrderItemRepository(ABC):
    @abstractmethod
    async def create_order_item(self, order_item: OrderItemCreate) -> OrderItem:
        """Persist a new order item."""
        pass
