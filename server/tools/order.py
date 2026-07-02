from pipecat.services.llm_service import FunctionCallParams

from state.order import OrderState

order_state = OrderState()

async def add_to_order(params: FunctionCallParams):
    """Add an item to the current order."""