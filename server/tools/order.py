from pipecat.services.llm_service import FunctionCallParams
from sqlalchemy.ext.asyncio import AsyncSession

from dtos.CustomerCreate import CustomerCreate
from dtos.OrderCreate import OrderCreate
from dtos.OrderItemCreate import OrderItemCreate
from models.customer import Customer, PaymentMode
from models.menu_item import MenuItem
from models.order import Order, OrderType
from models.order_item import OrderItem
from repositories.interfaces.conversation_repository import ConversationRepository
from repositories.interfaces.customer_repository import CustomerRepository
from repositories.interfaces.menu_repository import MenuRepository
from repositories.interfaces.order_item_repository import OrderItemRepository
from repositories.interfaces.order_repository import OrderRepository
from state.conversation import ConversationItem


def create_order_tools(
    conversation_repository: ConversationRepository,
    menu_repository: MenuRepository,
    customer_repository: CustomerRepository,
    order_repository: OrderRepository,
    order_item_repository: OrderItemRepository,
    session: AsyncSession,
):
    async def add_to_order(
        params: FunctionCallParams,
        item_name: str,
        quantity: int,
    ):
        """Add an item to the customer's order.

        Args:
            item_name: Name of the menu item.
            quantity: Number of items to add.
        """

        menu_item: MenuItem | None = await menu_repository.get_item_by_name(item_name)
        if menu_item is None:
            await params.result_callback(f"{item_name} is not available on our menu.")
            return

        if not menu_item.is_available:
            await params.result_callback(f"Sorry, {item_name} is currently unavailable.")
            return

        if not await conversation_repository.exists():
            await conversation_repository.create_conversation()

        conversation_item = ConversationItem(
            menu_item_id=menu_item.item_id,
            menu_item_name=menu_item.name,
            unit_price=float(menu_item.price),
            quantity=quantity,
        )
        # create a new order instance.. maybe initialize the order instance here.
        # here we will lazy init customer ... but how would the other tools know the customer we are talking about.???

        await conversation_repository.add_to_order(conversation_item)  # the in memory database.

        await params.result_callback(f"Added {quantity} {menu_item.name} to your order.")

    async def remove_from_order(
        params: FunctionCallParams,
        item_name: str,
    ):
        """Remove an item completely from the customer's order.

        Args:
            item_name: Name of the item to remove.
        """
        menu_item = await menu_repository.get_item_by_name(item_name)

        if menu_item is None:
            await params.result_callback("Item not found.")
            return

        removed = await conversation_repository.remove_from_order(menu_item.name)

        if removed:
            await params.result_callback(f"Removed {item_name} from your order.")
        else:
            await params.result_callback("Item not found in your order.")

    async def set_quantity(
        params: FunctionCallParams,
        item_name: str,
        quantity: int,
    ):
        """Set the quantity of an item."""

        menu_item = await menu_repository.get_item_by_name(item_name)

        if menu_item is None:
            await params.result_callback("Item not found.")
            return

        updated = await conversation_repository.set_quantity(
            menu_item.name,
            quantity,
        )

        if updated:
            await params.result_callback("Quantity updated.")
        else:
            await params.result_callback("Item not found in your order.")

    async def increase_quantity(
        params: FunctionCallParams,
        item_name: str,
        quantity: int,
    ):
        """Increase the quantity of an item."""

        menu_item = await menu_repository.get_item_by_name(item_name)

        if menu_item is None:
            await params.result_callback("Item not found.")
            return

        updated = await conversation_repository.increment_quantity(
            menu_item.name,
            quantity,
        )

        if updated:
            await params.result_callback(f"Added {quantity} more {item_name}.")
        else:
            await params.result_callback("Item not found in your order.")

    async def decrease_quantity(
        params: FunctionCallParams,
        item_name: str,
        quantity: int,
    ):
        """Decrease the quantity of an item."""

        menu_item = await menu_repository.get_item_by_name(item_name)

        if menu_item is None:
            await params.result_callback("Item not found.")
            return

        updated = await conversation_repository.decrement_quantity(
            menu_item.name,
            quantity,
        )

        if updated:
            await params.result_callback(f"Reduced {item_name} by {quantity}.")
        else:
            await params.result_callback("Item not found in your order.")

    async def get_order(params: FunctionCallParams):
        """Return the customer's current order."""
        conversation = await conversation_repository.get_conversation()
        await params.result_callback([item.model_dump() for item in conversation.items])

    async def get_bill(params: FunctionCallParams):
        """Return the total bill for the customer's current order."""

        total = await conversation_repository.get_bill()
        await params.result_callback(
            {
                "total": total,
            }
        )

    async def update_conversation_details(
        params: FunctionCallParams,
        customer_name: str | None = None,
        customer_contact: str | None = None,
        delivery_address: str | None = None,
    ):
        """Update any customer details collected during the conversation."""

        if customer_name is not None:
            await conversation_repository.set_customer_name(customer_name)

        if customer_contact is not None:
            await conversation_repository.set_customer_contact(customer_contact)

        if delivery_address is not None:
            await conversation_repository.set_delivery_address(delivery_address)

        await params.result_callback("Customer details updated.")

    async def set_order_type(
        params: FunctionCallParams,
        order_type: str,
    ):
        """Set the customer's order type."""

        try:
            await conversation_repository.set_order_type(OrderType(order_type.lower()))
        except ValueError:
            await params.result_callback(
                "Invalid order type. Choose one of: takeaway, delivery, dine_in."
            )
            return

        await params.result_callback(f"Order type set to {order_type}.")

    async def confirm_order(params: FunctionCallParams):
        """
        Confirm and place the customer's order.

        Only call this tool after all required customer and order
        details have been collected.

        For takeaway:
        - Customer name
        - Phone number

        For delivery:
        - Customer name
        - Phone number
        - Delivery address

        Do not call this tool if any required information is missing.
        """
        conversation = await conversation_repository.get_conversation()
        # Create customer

        customer = CustomerCreate(
            name=conversation.customer_name,
            phone=conversation.phone_number,
            address=conversation.delivery_address,
            payment_mode=PaymentMode.CASH,  # TODO: change this to accept this from the user conversation
        )

        try:
            customer_created = await customer_repository.get_by_phone(
                conversation.phone_number,
            )

            if customer_created is None:
                customer_created = await customer_repository.create_customer(customer)

            total_bill_amount = await conversation_repository.get_bill()

            order = OrderCreate(
                customer_id=customer_created.customer_id,
                order_type=conversation.order_type,
                total_bill_amount=total_bill_amount,
            )

            order_created = await order_repository.create_order(order)

            for item in conversation.items:
                order_item = OrderItemCreate(
                    order_id=order_created.order_id,
                    menu_item_id=item.menu_item_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )

                await order_item_repository.create_order_item(order_item)

            await conversation_repository.delete_conversation()
            print("Before commit")

            await session.commit()
            print("After commit")

            await params.result_callback("Your order has been placed successfully.")
            print("After result_callback")

        except Exception:
            await session.rollback()

            raise

    return [
        add_to_order,
        remove_from_order,
        set_quantity,
        increase_quantity,
        decrease_quantity,
        get_order,
        get_bill,
        confirm_order,
        set_order_type,
        update_conversation_details,
    ]
