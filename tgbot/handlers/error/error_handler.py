import logging
from aiogram.types import Update
from aiogram import Dispatcher
from aiogram.utils.exceptions import *


async def error_handler(update: Update, exception: BadRequest):
    if isinstance(exception, CantDemoteChatCreator):
        logging.debug('Can`t demote chat creator')
        return True

    if isinstance(exception, MessageNotModified):
        logging.debug('Message is not modified')
        return True

    if isinstance(exception, MessageCantBeDeleted):
        logging.info('Message cant be modified')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logging.info('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logging.info('Message text is empty')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logging.debug('Message text is empty')
        return True

    if isinstance(exception, Unauthorized):
        logging.info(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        logging.info(f'InvalidQueryID: {exception}\nUpdate: {update}')
        return True

    if isinstance(exception, CantParseEntities):
        await update.message.answer(f'Cant parse entities: {exception}')
        return True

    if isinstance(exception, RetryAfter):
        logging.exception(f'Retry after: {exception}\nUpdate: {update}')
        return True

    if isinstance(exception, BadRequest):
        logging.exception(f'Bad request: {exception}\nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception(f'Telegram API Error: {exception}\nUpdate: {update}')
        return True

    logging.exception(f'Update error: {exception}\nUpdate: {update}')


def register_error_handler(dp: Dispatcher):
    dp.register_errors_handler(callback=error_handler)
