from sqlalchemy import select
from sqlalchemy.orm import Session

from models.order import Order
from repositories.interfaces.order_repository import OrderRepository


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session):
        self._session = session

    def create_order(self, order: Order) -> Order:
        # order is created the first time user adds something to his order.
        statement = select(Order).where(Order.name == item_name)

        return self._session.execute(statement).scalar_one_or_none()
    
    def update_order(self, order: Order) -> None:
        pass