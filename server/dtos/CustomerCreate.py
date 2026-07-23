from pydantic import BaseModel

from models.customer import PaymentMode


class CustomerCreate(BaseModel):
    name: str
    phone: str
    address: str
    payment_mode: PaymentMode
