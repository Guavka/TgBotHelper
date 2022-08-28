import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config, Config
from tgbot.filters.isAdmin import AdminFilter

from tgbot.handlers.private.admin import register_admin_private
from tgbot.handlers.private.user import register_user_private
from tgbot.handlers.error.error_handler import register_error_handler

from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.middlewares.big_brother import BigBrother

logger = logging.getLogger(__name__)


def register_all_middlewares(dp: Dispatcher, config: Config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(BigBrother(config=config))


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)


def register_private_handlers(dp: Dispatcher):
    register_admin_private(dp)
    register_user_private(dp)


def register_all_handlers(dp: Dispatcher):
    register_private_handlers(dp)
    register_error_handler(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.get_session().close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
