from pipecat.services.llm_service import FunctionCallParams

from repositories.interfaces.conversation_repository import ConversationRepository
from repositories.interfaces.customer_repository import CustomerRepository
from repositories.interfaces.menu_repository import MenuRepository
from state.conversation import ConversationItem
from state.order import OrderItem, OrderState


def create_order_tools(
    conversation_repository: ConversationRepository, menu_repository: MenuRepository, customer_repository: CustomerRepository
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

        menu_item = await menu_repository.get_item_by_name(item_name)
        if menu_item is None:
            await params.result_callback(f"{item_name} is not available on our menu.")
            return

        if not menu_item.is_available:
            await params.result_callback(f"Sorry, {item_name} is currently unavailable.")
            return

        if not await conversation_repository.exists():
            await conversation_repository.create_conversation()

        conversation_item = ConversationItem(
            menu_item_id=menu_item.menu_item_id,
            menu_item_name=menu_item.name,
            unit_price=float(menu_item.price),
            quantity=quantity,
        )
        # create a new order instance.. maybe initialize the order instance here.
        # here we will lazy init customer ... but how would the other tools know the customer we are talking about.???
        # order_repository.add_to_order(item_name, quantity)
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

        removed = await conversation_repository.remove_from_order(item_name)
        if removed:
            print(f"{item_name} removed sucessfully from your order.")
            await params.result_callback(f"Removed {item_name} from your order.")

        else:
            print(f"Couldn't find {item_name} in your orders to remove.")
            await params.result_callback("Item not found.")

    async def set_quantity(params: FunctionCallParams, item_name: str, quantity: int):
        """Set the quantity of an item in the customer's order.

        Args:
            item_name: Name of the item whose quantity should be changed.
            quantity: The new quantity for the item.
        """
        set = await conversation_repository.set_quantity(item_name, quantity)
        if set:
            await params.result_callback("Quantity set.")
        else:
            await params.result_callback("Menu item not found in your order to set the quantity.")

    async def get_order(params: FunctionCallParams):
        """Return the customer's current order."""
        order = await conversation_repository.get_conversation()
        await params.result_callback(f"Your order: {order}")

    async def get_bill(params: FunctionCallParams):
        """Return the total bill for the customer's current order."""

        bill = await conversation_repository.get_bill()
        await params.result_callback(
            {
                "total": bill,
            }
        )

    async def confirm_order(params: FunctionCallParams):
        """Confirm and place the customer's current order."""
        # flow: when confirm order is done, order repository is supposed to be called, customer repository is supposed to be called.
        # create a new customer, create a new order, wire in the customer's id into the order table as FK.
        # and then clear the redis.
        # so first of all, to create a customer, get all the customer details.. create a json.. pass it in the create_customer method right below.
        customer_details = conversation_repository
        customer = customer_repository.create_customer()
        await conversation_repository.confirm_order()
        await params.result_callback("Your order has been placed successfully.")

    async def increase_quantity(params: FunctionCallParams, menu_item: str, quantity: int):
        await conversation_repository.increment_quantity(menu_item, quantity)
        await params.result_callback(
            f"The quantity of {menu_item} has been increased by {quantity}"
        )

    async def decrease_quantity(params: FunctionCallParams, menu_item: str, quantity: int):
        await conversation_repository.decrement_quantity(menu_item, quantity)
        await params.result_callback(
            f"The quantity of {menu_item} has been decreased by {quantity}"
        )

    async def ask_customer_details(params: FunctionCallParams):
        """Prompt the user to provide their details to the LLM. when the user then provides their details to the LLM, store it in a redis state, perhaps the conversation state needs to """

    return [
        add_to_order,
        remove_from_order,
        set_quantity,
        increase_quantity,
        decrease_quantity,
        get_order,
        get_bill,
        confirm_order,
        ask_customer_details
    ]
