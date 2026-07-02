from pipecat.services.llm_service import FunctionCallParams

MENU = [
    {"name": "Margherita Pizza", "price": 299},
    {"name": "Veg Burger", "price": 199},
    {"name": "Coke", "price": 60},
]


async def get_menu(params: FunctionCallParams):
    """Return the restaurant menu."""

    await params.result_callback(MENU)