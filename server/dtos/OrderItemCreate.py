from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    order_id: int
    menu_item_id: int
    quantity: int
    unit_price: float
