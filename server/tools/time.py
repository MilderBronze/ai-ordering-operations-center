from datetime import datetime

from pipecat.services.llm_service import FunctionCallParams


async def get_current_time(params: FunctionCallParams):
    """Return the current local time in HH:MM AM/PM format."""

    current_time = datetime.now().strftime("%I:%M %p")

    await params.result_callback(current_time)