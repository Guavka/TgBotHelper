from aiogram import Dispatcher
from tgbot.handlers.private.user.start import register_user_start
from tgbot.handlers.private.user.help import register_user_help
from tgbot.handlers.private.user.invite import register_user_invite
from tgbot.handlers.private.user.test import register_user_test


def register_user_private(dp: Dispatcher):
    register_user_start(dp)
    register_user_help(dp)
    register_user_invite(dp)
    register_user_test(dp)
