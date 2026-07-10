from abc import ABC, abstractmethod

from state.conversation import ConversationItem, ConversationState


class ConversationRepository(ABC):
    @abstractmethod
    def create_conversation(self) -> None:
        """Create and persist a new conversation."""
        pass

    @abstractmethod
    def add_to_order(self, item: ConversationItem) -> None:
        """Add an item to the current order."""
        pass

    @abstractmethod
    def remove_from_order(self, menu_item: str) -> None:
        """Remove an item completely from the current order."""
        pass

    @abstractmethod
    def increment_quantity(self, menu_item: str, quantity: int) -> bool:
        """Change the quantity of an item."""
        pass

    @abstractmethod
    def decrement_quantity(self, menu_item: str, quantity: int) -> bool:
        """Change the quantity of an item."""
        pass

    @abstractmethod
    def set_quantity(self, menu_item: str, quantity: int) -> bool:
        """Change the quantity of an item."""
        pass

    @abstractmethod
    def get_conversation(self) -> ConversationState:
        """Return the current conversation."""
        pass

    @abstractmethod
    def get_bill(self) -> float:
        """Return the current bill."""
        pass

    @abstractmethod
    def delete_conversation(self) -> None:
        """Delete the conversation."""
        pass

    @abstractmethod
    def exists(self) -> bool:
        """check if conversation exists"""
