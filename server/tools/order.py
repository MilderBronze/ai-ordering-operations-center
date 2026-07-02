from pipecat.services.llm_service import FunctionCallParams
from server.tools.menu import MENU

from state.order import OrderItem, OrderState


def find_menu_item(item_name: str):
    return next(
        (item for item in MENU if item["name"] == item_name),
        None,
    )


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

        menu_item = find_menu_item(item_name)

        if menu_item is None:
            await params.result_callback(f"{item_name} is not available on our menu.")
            return

        if not menu_item["is_available"]:
            await params.result_callback(f"Sorry, {item_name} is currently unavailable.")
            return

        for item in order_state.items:
            if item.item_name == item_name:
                item.quantity += quantity

                print(f"Order status: {order_state.items}")

                await params.result_callback("Added.")
                return

        order_state.items.append(
            OrderItem(
                item_name=item_name,
                quantity=quantity,
            )
        )

        print(f"Order status: {order_state.items}")

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

        print(f"Order status: {order_state.items}")

        await params.result_callback("Removed.")

    async def change_quantity(
        params: FunctionCallParams,
        item_name: str,
        quantity: int,
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

        print(f"Order status: {order_state.items}")

        await params.result_callback("Quantity changed.")

    async def get_order(
        params: FunctionCallParams,
    ):
        """Return the customer's current order."""

        await params.result_callback(order_state.items)

    async def get_bill(
        params: FunctionCallParams,
    ):
        """Return the total bill for the customer's current order."""

        total = 0

        for item in order_state.items:
            menu_item = find_menu_item(item.item_name)

            if menu_item:
                total += menu_item["price"] * item.quantity

        await params.result_callback(
            {
                "total": total,
            }
        )

    async def confirm_order(
        params: FunctionCallParams,
    ):
        """Confirm and place the customer's current order."""

        print(order_state)

        await params.result_callback(
            "Your order has been placed successfully."
        )

    return [
        add_to_order,
        remove_from_order,
        change_quantity,
        get_order,
        get_bill,
        confirm_order
    ]
