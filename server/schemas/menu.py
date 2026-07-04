from pydantic import BaseModel


class MenuItemResponse(BaseModel):
    name: str
    price: float
    is_available: bool