# contains the pydantic schema for Customer model
from pydantic import BaseModel


def CustomerModel(BaseModel):
    name=str,
    address=str,
