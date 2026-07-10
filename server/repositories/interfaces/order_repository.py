from abc import ABC, abstractmethod


class OrderRepository(ABC):
    @abstractmethod
    def add_to_order(
        self,
        item_name: str,
        quantity: int,
    ):
        pass

    @abstractmethod
    def remove_from_order(
        self,
        item_name: str,
    ):
        pass

    @abstractmethod
    def change_quantity(
        self,
        item_name: str,
        quantity: int,
    ):
        pass

    @abstractmethod
    def get_order(self): # the return type for this is subject to change. will unfold naturally. i know this is wrong right now.
        pass

    @abstractmethod
    def confirm_order(self):
        pass
