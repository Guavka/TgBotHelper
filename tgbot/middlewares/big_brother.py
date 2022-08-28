import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler

from tgbot.config import Config


class BigBrother(BaseMiddleware):
    def __init__(self, **kwargs):
        super().__init__()
        self.__config: Config = kwargs.get('config')

    async def on_pre_process_update(self, update: types.Update, data: dict):
        logging.info('[---------New update---------]')
        logging.info('1.Pre process update')
        data['middleware_data'] = 'This data go to on_post_process_update'

        if update.message:
            user = update.message.from_user.id
        elif update.callback_query:
            user = update.callback_query.from_user.id
        else:
            return

        if user in self.__config.tg_bot.banned_ids:
            await update.message.answer('You was banned!')
            raise CancelHandler()

    async def on_process_update(self, update: types.Update, data: dict):
        logging.info('2.Process update')

    async def on_pre_process_message(self, update: types.Update, data: dict):
        logging.info('3.Pre process message')
        data['middleware_data'] = 'This data go to on_post_process_message'