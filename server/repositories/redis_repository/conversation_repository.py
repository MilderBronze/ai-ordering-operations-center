import json
import uuid

import redis.asyncio as redis

from repositories.interfaces.conversation_repository import ConversationRepository
from state.conversation import ConversationItem, ConversationState


class RedisConversationRepository(ConversationRepository):
    def __init__(self, redis_client: redis.Redis):
        self._redis = redis_client
        self._conversation_id: str | None = None
        # this means that the class RedisConversationRepository will have all the methods in ConversationRepostiroy and also 2 additional properties namely _redis and _conversation_id

    async def create_conversation(self) -> ConversationState:
        """sets redis too"""
        conversation = ConversationState(conversation_id=str(uuid.uuid4()))
        self._conversation_id = conversation.conversation_id

        await self.save_conversation(conversation)

        return conversation

    async def get_conversation(self) -> ConversationState:
        conversation_json = await self._redis.get(f"conversation:{self._conversation_id}")
        if conversation_json is None:
            raise ValueError("Conversation not found")

        return ConversationState.model_validate_json(conversation_json)

    async def get_bill(self):
        conversation = await self.get_conversation()
        bill_amount = 0
        for item in conversation.items:
            bill_amount += item.quantity * item.unit_price

    async def delete_conversation(self):
        # get the id of the current conversation and then delete it from redis store
        # get the id of the current conversation:
        conversation_id = self._conversation_id
        self._redis.delete(conversation_id)

    async def add_to_order(self, conversation_item: ConversationItem):
        conversation = await self.get_conversation()

        for item in conversation.items:
            if item.menu_item_id == conversation_item.menu_item_id:
                item.quantity += conversation_item.quantity
                await self._save_conversation(conversation)
                return

        conversation.items.append(conversation_item)
        await self._save_conversation(conversation)

    async def set_quantity(self, menu_item: str, quantity: int) -> bool:
        conversation = await self.get_conversation()

        for item in conversation.items:
            if item.menu_item_name == menu_item:
                item.quantity = quantity
                await self._save_conversation(conversation)
                return True
        return False

    async def increment_quantity(self, menu_item: str, quantity: int) -> bool:
        conversation = await self.get_conversation()

        for item in conversation.items:
            if item.menu_item_name == menu_item:
                item.quantity += quantity

                if item.quantity <= 0:
                    conversation.items.remove(item)

                await self._save_conversation(conversation)
                return True
        return False

    async def decrement_quantity(self, menu_item: str, quantity: int) -> bool:
        conversation = await self.get_conversation()

        for item in conversation.items:
            if item.menu_item_name == menu_item:
                item.quantity -= quantity
                await self._save_conversation(conversation)
                return True
        return False

    async def remove_from_order(self, menu_item):
        conversation = await self.get_conversation()
        order_items = conversation.items
        for item in order_items:
            if item.menu_item_name == menu_item:
                order_items.remove(item)
                await self.save_conversation(conversation)
                return True
        return False

    async def exists(self) -> bool:
        return self._conversation_id is not None

    async def _save_conversation(self, conversation: ConversationState):
        await self._redis.set(
            f"conversation:{conversation.conversation_id}",
            conversation.model_dump_json(),
        )
