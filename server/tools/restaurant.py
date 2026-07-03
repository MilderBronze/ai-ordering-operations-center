from datetime import datetime

from pipecat.services.llm_service import FunctionCallParams

from config import CLOSING_HOUR, OPENING_HOUR


async def is_restaurant_open(params: FunctionCallParams):
    """Return whether Spice Garden is currently open."""
    now = datetime.now()

    is_open = OPENING_HOUR <= now.hour < CLOSING_HOUR

    message = (
        "Yes, Spice Garden is currently open."
        if is_open
        else "No, Spice Garden is currently closed."
    )

    await params.result_callback(message)