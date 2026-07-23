import uuid

import redis.asyncio as redis

from models.order import OrderType
from repositories.interfaces.conversation_repository import ConversationRepository
from state.conversation import ConversationItem, ConversationState


class RedisConversationRepository(ConversationRepository):
    def __init__(self, redis_client: redis.Redis):
        self._redis = redis_client
        self._conversation_id: str | None = None

    async def create_conversation(self) -> ConversationState:
        conversation = ConversationState(conversation_id=str(uuid.uuid4()))

        self._conversation_id = conversation.conversation_id

        await self._save_conversation(conversation)

        return conversation

    async def get_conversation(self) -> ConversationState:

        if self._conversation_id is None:
            raise ValueError("No active conversation.")

        conversation_json = await self._redis.get(f"conversation:{self._conversation_id}")

        if conversation_json is None:
            raise ValueError("Conversation not found.")

        return ConversationState.model_validate_json(conversation_json)

    async def _ensure_conversation(self) -> ConversationState:

        if self._conversation_id is None:
            return await self.create_conversation()

        conversation_json = await self._redis.get(f"conversation:{self._conversation_id}")

        if conversation_json is None:
            return await self.create_conversation()

        return ConversationState.model_validate_json(conversation_json)

    async def _save_conversation(
        self,
        conversation: ConversationState,
    ) -> None:

        await self._redis.set(
            f"conversation:{conversation.conversation_id}",
            conversation.model_dump_json(),
        )

    async def exists(self) -> bool:

        if self._conversation_id is None:
            return False

        return (await self._redis.exists(f"conversation:{self._conversation_id}")) == 1

    async def get_bill(self) -> float:

        conversation = await self.get_conversation()

        return sum(item.quantity * item.unit_price for item in conversation.items)

    async def delete_conversation(self) -> None:

        if self._conversation_id is None:
            return

        await self._redis.delete(f"conversation:{self._conversation_id}")

        self._conversation_id = None

    async def add_to_order(
        self,
        conversation_item: ConversationItem,
    ) -> None:

        conversation = await self._ensure_conversation()

        for item in conversation.items:
            if item.menu_item_id == conversation_item.menu_item_id:
                item.quantity += conversation_item.quantity

                await self._save_conversation(conversation)

                return

        conversation.items.append(conversation_item)

        await self._save_conversation(conversation)

    async def set_quantity(
        self,
        menu_item: str,
        quantity: int,
    ) -> bool:

        conversation = await self._ensure_conversation()

        for item in conversation.items:
            if item.menu_item_name == menu_item:
                item.quantity = quantity

                await self._save_conversation(conversation)

                return True

        return False

    async def increment_quantity(
        self,
        menu_item: str,
        quantity: int,
    ) -> bool:

        conversation = await self._ensure_conversation()

        for item in conversation.items:
            if item.menu_item_name == menu_item:
                item.quantity += quantity

                await self._save_conversation(conversation)

                return True

        return False

    async def decrement_quantity(
        self,
        menu_item: str,
        quantity: int,
    ) -> bool:

        conversation = await self._ensure_conversation()

        for item in conversation.items:
            if item.menu_item_name == menu_item:
                item.quantity -= quantity

                if item.quantity <= 0:
                    conversation.items.remove(item)

                await self._save_conversation(conversation)

                return True

        return False

    async def remove_from_order(
        self,
        menu_item: str,
    ) -> bool:

        conversation = await self._ensure_conversation()

        for item in conversation.items:
            if item.menu_item_name == menu_item:
                conversation.items.remove(item)

                await self._save_conversation(conversation)

                return True

        return False

    async def set_delivery_address(
        self,
        address: str,
    ) -> bool:

        conversation = await self._ensure_conversation()

        conversation.delivery_address = address

        await self._save_conversation(conversation)

        return True

    async def set_customer_contact(
        self,
        contact: str,
    ) -> bool:

        conversation = await self._ensure_conversation()

        conversation.phone_number = contact

        await self._save_conversation(conversation)

        return True

    async def set_customer_name(
        self,
        name: str,
    ) -> bool:

        conversation = await self._ensure_conversation()

        conversation.customer_name = name

        await self._save_conversation(conversation)

        return True

    async def set_order_type(
        self,
        order_type: OrderType,
    ) -> bool:

        conversation = await self._ensure_conversation()

        conversation.order_type = order_type

        await self._save_conversation(conversation)

        return True
