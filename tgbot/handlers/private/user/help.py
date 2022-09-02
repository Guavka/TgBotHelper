from aiogram.types import Message, ChatType
from aiogram import Dispatcher
from tgbot.misc.throttling import rate_limit

@rate_limit(3)
async def user_help(message: Message):
    await message.answer("Краткая справка по использования бота:\n\
Команда '/start' инициализирует работу бота (начало работы)\n\
Команда '/help' вызывает краткую справку\n\
Команда '/invite' генерирует ссылку для привлечения рефералов")


def register_user_help(dp: Dispatcher):
    dp.register_message_handler(
        user_help, commands=["help"], state="*", chat_type=ChatType.PRIVATE)
