from abc import ABC, abstractmethod

from models.order import OrderType
from state.conversation import ConversationItem, ConversationState


class ConversationRepository(ABC):
    @abstractmethod
    async def create_conversation(self) -> ConversationState:
        """Create and persist a new conversation."""
        pass

    @abstractmethod
    async def add_to_order(self, item: ConversationItem) -> None:
        """Add an item to the current order."""
        pass

    @abstractmethod
    async def remove_from_order(self, menu_item: str) -> bool:
        """Remove an item completely from the current order."""
        pass

    @abstractmethod
    async def increment_quantity(
        self,
        menu_item: str,
        quantity: int,
    ) -> bool:
        """Increase quantity of an item."""
        pass

    @abstractmethod
    async def decrement_quantity(
        self,
        menu_item: str,
        quantity: int,
    ) -> bool:
        """Decrease quantity of an item."""
        pass

    @abstractmethod
    async def set_quantity(
        self,
        menu_item: str,
        quantity: int,
    ) -> bool:
        """Set quantity of an item."""
        pass

    @abstractmethod
    async def get_conversation(self) -> ConversationState:
        """Return the current conversation."""
        pass

    @abstractmethod
    async def get_bill(self) -> float:
        """Return the current bill."""
        pass

    @abstractmethod
    async def delete_conversation(self) -> None:
        """Delete the current conversation."""
        pass

    @abstractmethod
    async def exists(self) -> bool:
        """Check whether a conversation exists."""
        pass

    @abstractmethod
    async def set_delivery_address(self, address: str) -> bool:
        """Update delivery address."""
        pass

    @abstractmethod
    async def set_customer_contact(self, contact: str) -> bool:
        """Update customer contact."""
        pass

    @abstractmethod
    async def set_customer_name(self, name: str) -> bool:
        """Update customer name."""
        pass

    @abstractmethod
    async def set_order_type(self, order_type: OrderType) -> bool:
        """Update order type."""
        pass
