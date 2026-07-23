from abc import ABC, abstractmethod

from models.menu_item import MenuItem


class MenuRepository(ABC):

    @abstractmethod
    async def get_item_by_name(self, item_name: str) -> MenuItem | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[MenuItem] | None:
        # None in case menu table is empty
        pass

    @abstractmethod
    async def create(self, menu_item: MenuItem) -> MenuItem:
        pass

    @abstractmethod
    async def delete(self, item_id: int) -> None:
        pass