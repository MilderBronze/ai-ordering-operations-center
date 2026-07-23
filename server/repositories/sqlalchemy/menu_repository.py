from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.menu_item import MenuItem
from repositories.interfaces.menu_repository import MenuRepository


class SqlAlchemyMenuRepository(MenuRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_item_by_name(self, item_name: str) -> MenuItem | None:
        statement = select(MenuItem).where(func.lower(MenuItem.name) == item_name.lower())

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_all(self) -> list[MenuItem]:
        statement = select(MenuItem)

        result = await self._session.execute(statement)

        return result.scalars().all()

    async def create(self, menu_item: MenuItem) -> MenuItem:
        self._session.add(menu_item)

        await self._session.flush()
        await self._session.refresh(menu_item)

        return menu_item

    async def delete(self, item_id: int) -> bool:

        statement = select(MenuItem).where(MenuItem.item_id == item_id)
        result = await self._session.execute(statement)

        menu_item = result.scalar_one_or_none()

        if menu_item is None:
            return False

        await self._session.delete(menu_item)

        return True
