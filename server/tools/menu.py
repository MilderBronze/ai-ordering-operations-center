from pipecat.services.llm_service import FunctionCallParams

from repositories.interfaces.menu_repository import MenuRepository
from schemas.menu import MenuItemResponse


def create_menu_tools(menu_repository: MenuRepository):

    async def get_menu(params: FunctionCallParams):
        """Return the restaurant menu."""

        menu = await menu_repository.get_all()
        await params.result_callback(
            [
                MenuItemResponse(
                    name=item.name,
                    price=float(item.price),
                    is_available=item.is_available,
                ).model_dump()
                for item in menu
            ]
        )

    return [get_menu]
