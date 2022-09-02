from aiogram.types import Message, ChatType
from aiogram import Dispatcher
from aiogram.utils.deep_linking import get_start_link
from tgbot.misc.throttling import rate_limit

@rate_limit(3)
async def user_link(message: Message):
    link = await get_start_link(message.from_id, encode=True)
    await message.answer(f"Hello, {message.chat.first_name}!\nYour start link is {link}")


def register_user_invite(dp: Dispatcher):
    dp.register_message_handler(
        user_link, commands=["invite"], state="*", chat_type=ChatType.PRIVATE)
