from models.customer import Customer
from repositories.interfaces.customer_repository import CustomerRepository


class SqlAlchemyCustomerRepository(CustomerRepository):
    def create_customer(self) -> Customer:
        # create new customer

        # write the sqlalchemy way of creating a new customer using the pydantic base model
        
        pass
