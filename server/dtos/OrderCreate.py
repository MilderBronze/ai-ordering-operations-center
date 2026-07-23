from pydantic import BaseModel

from models.order import OrderType


class OrderCreate(BaseModel):
    customer_id: int
    order_type: OrderType
    total_bill_amount: float