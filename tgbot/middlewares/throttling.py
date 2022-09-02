import asyncio
from typing import Union
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import Throttled
from aiogram import Dispatcher


from tgbot.misc.throttling import throttling_key, throttling_rate_limit


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood'):
        self.limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def throttle(self, target: Union[Message, CallbackQuery]):
        handler = current_handler.get()
        if not handler:
            return

        limit = getattr(handler, throttling_rate_limit, self.limit)
        key = getattr(handler, throttling_key,
                      f'{self.prefix}_{handler.__name__}')

        dp = Dispatcher.get_current()
        try:
            await dp.throttle(key, rate=limit)
        except Throttled as t:
            await self.target_throttled(target, t, dp, key)
            raise CancelHandler()

    @staticmethod
    async def target_throttled(target: Union[Message, CallbackQuery], throttled: Throttled, dispatcher: Dispatcher, key: str):
        msg = target.message if isinstance(target, CallbackQuery) else target
        delta = throttled.rate-throttled.delta
        if throttled.exceeded_count == 2:
            await msg.reply('Слишком часто')
        elif throttled.exceeded_count == 3:
            await msg.reply(f'Ждите {delta} секунд')
        await asyncio.sleep(delta)

        thr = await dispatcher.check_key(key)
        if thr.exceeded_count == throttled.exceeded_count:
            await msg.reply('Ожидание завершено')

    async def on_process_message(self, message, data):
        await self.throttle(message)

    async def on_process_callback_query(self, call, data):
        await self.throttle(call)
