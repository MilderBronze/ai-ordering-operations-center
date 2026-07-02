from pipecat.services.llm_service import FunctionCallParams

from state.order import OrderItem, OrderState

def create_order_tools(order_state: OrderState):

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
        for item in order_state.items:
            if item.item_name == item_name:
                item.quantity += quantity
                await params.result_callback("Added.")
                return

        order_state.items.append(
            OrderItem(
                item_name=item_name,
                quantity=quantity,
            )
        )

        print(f"order status: {order_state.items}")
        await params.result_callback("Added.")


    async def remove_from_order(
        params: FunctionCallParams,
        item_name: str,
    ):
        """Remove an item completely from the customer's order.

        Args:
            item_name: Name of the item to remove.
        """

        for item in order_state.items:
            if item.item_name == item_name:
                order_state.items.remove(item)
                break

        print(f"Item removed: {item_name}")
        print(f"order status: {order_state.items}")

        await params.result_callback("Removed.")

    async def change_quantity(
            params: FunctionCallParams,
            item_name: str,
            quantity: int
    ):
        """Change the quantity of an item in the customer's order.

        Args:
            item_name: Name of the item whose quantity should be changed.
            quantity: The new quantity for the item.
        """
        for item in order_state.items:
            if item.item_name == item_name:
                item.quantity = quantity
                break

        print(f"quantity of the item {item_name} changed to {quantity}")
        
        await params.result_callback("Quantity changed.")

    async def get_order(
        params: FunctionCallParams,
    ):
        """Return the customer's current order."""

        await params.result_callback(order_state.items)

    return [
        add_to_order,
        remove_from_order,
        change_quantity,
        get_order
    ]