from sqlalchemy import select
from sqlalchemy.orm import Session

from models.menu_item import MenuItem
from repositories.interfaces.menu_repository import MenuRepository


class SqlAlchemyMenuRepository(MenuRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_item_by_name(self, item_name: str) -> MenuItem | None:

        statement = select(MenuItem).where(MenuItem.name == item_name)

        return self._session.execute(statement).scalar_one_or_none()

    def get_all(self) -> list[MenuItem]:

        statement = select(MenuItem)

        return self._session.execute(statement).scalars().all()

    def create(self, menu_item: MenuItem) -> MenuItem:

        self._session.add(menu_item)
        # self._session.commit()
        # self._session.refresh(menu_item)

        return menu_item

    def update(self, menu_item: MenuItem) -> MenuItem:

        # self._session.commit()
        # self._session.refresh(menu_item)

        return menu_item

    def delete(self, item_id: int) -> bool:

        statement = select(MenuItem).where(MenuItem.item_id == item_id)

        menu_item = self._session.execute(statement).scalar_one_or_none()

        if menu_item is None:
            return False

        self._session.delete(menu_item)
        # self._session.commit()

        return True
