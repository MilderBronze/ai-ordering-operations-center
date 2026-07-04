from abc import ABC, abstractmethod

from models.menu_item import MenuItem


class MenuRepository(ABC):

    @abstractmethod
    def get_item_by_name(self, item_name: str) -> MenuItem | None:
        pass

    @abstractmethod
    def get_all(self) -> list[MenuItem] | None: # none in case menu table is all empty
        pass

    @abstractmethod
    def create(self, menu_item: MenuItem) -> MenuItem:
        pass

    @abstractmethod
    def update(self, menu_item: MenuItem) -> MenuItem:
        pass

    @abstractmethod
    def delete(self, item_id: int) -> None:
        pass