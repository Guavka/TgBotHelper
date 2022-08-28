from aiogram import Dispatcher
from tgbot.handlers.private.admin.start import register_admin_start


def register_admin_private(dp: Dispatcher):
    register_admin_start(dp)
