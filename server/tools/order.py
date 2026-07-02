from pipecat.services.llm_service import FunctionCallParams

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

    print(item_name, quantity)

    await params.result_callback("Added.")

async def remove_from_order(
    params: FunctionCallParams,
    item_name: str,
):
    """Remove an item completely from the customer's order.

    Args:
        item_name: Name of the item to remove.
    """

    print(f"Item removed: {item_name}")

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
    print(f"quantity of the item {item_name} changed to {quantity}")
    
    await params.result_callback("Quantity changed.")
