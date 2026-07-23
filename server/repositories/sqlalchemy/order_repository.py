from sqlalchemy.ext.asyncio import AsyncSession

from dtos import OrderCreate
from models.order import Order
from repositories.interfaces.order_repository import OrderRepository


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_order(self, order: OrderCreate) -> Order:
        orm_order = Order(**order.model_dump())

        self._session.add(orm_order)

        await self._session.flush()
        await self._session.refresh(orm_order)

        return orm_order
