from pipecat.services.llm_service import FunctionCallParams

MENU = [
    {
        "name": "Margherita Pizza",
        "price": 299,
        "is_available": True,
    },
    {
        "name": "Veg Burger",
        "price": 199,
        "is_available": True,
    },
    {
        "name": "Coke",
        "price": 60,
        "is_available": False,
    },
]


async def get_menu(params: FunctionCallParams):
    """Return the restaurant menu."""

    await params.result_callback(MENU)
