from pydantic import BaseModel, Field

from models.order import OrderType


class ConversationItem(BaseModel):
    menu_item_id: int
    menu_item_name: str
    unit_price: float
    quantity: int


class ConversationState(BaseModel):
    conversation_id: str
    items: list[ConversationItem] = Field(default_factory=list)
    customer_name: str | None = None
    phone_number: str | None = None
    order_type: OrderType | None = None
    delivery_address: str | None = None
