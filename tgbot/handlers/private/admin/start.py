from aiogram import Dispatcher
from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import CommandStart
from tgbot.misc.throttling import rate_limit


@rate_limit(3)
async def admin_start(message: Message):
    await message.reply("Hello, admin!")


def register_admin_start(dp: Dispatcher):
    dp.register_message_handler(
        admin_start,
        CommandStart(),
        state="*",
        is_admin=True,
        chat_type=ChatType.PRIVATE)
