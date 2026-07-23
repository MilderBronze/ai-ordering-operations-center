from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dtos import CustomerCreate
from models.customer import Customer
from repositories.interfaces.customer_repository import CustomerRepository


class SqlAlchemyCustomerRepository(CustomerRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_customer(
        self,
        customer: CustomerCreate,
    ) -> Customer:

        orm_customer = Customer(**customer.model_dump())

        self._session.add(orm_customer)

        await self._session.flush()
        await self._session.refresh(orm_customer)

        return orm_customer
    
    async def get_by_phone(
        self,
        phone: str,
    ) -> Customer | None:

        result = await self._session.execute(
            select(Customer).where(Customer.phone == phone)
        )

        return result.scalar_one_or_none()