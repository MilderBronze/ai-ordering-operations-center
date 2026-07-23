from sqlalchemy.ext.asyncio import AsyncSession

from dtos import OrderItemCreate
from models.order_item import OrderItem
from repositories.interfaces.order_item_repository import OrderItemRepository


class SqlAlchemyOrderItemRepository(OrderItemRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_order_item(
        self,
        order_item: OrderItemCreate,
    ) -> OrderItem:

        orm_order_item = OrderItem(
            order_id=order_item.order_id,
            item_id=order_item.menu_item_id,
            quantity=order_item.quantity,
            unit_price=order_item.unit_price,
        )

        self._session.add(orm_order_item)

        await self._session.flush()
        await self._session.refresh(orm_order_item)

        return orm_order_item
