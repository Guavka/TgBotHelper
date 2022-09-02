from aiogram import Dispatcher
from aiogram.types import Message, ChatType
from aiogram.utils.markdown import hcode
from tgbot.states.test import Test
from aiogram.dispatcher import FSMContext
from tgbot.misc.throttling import rate_limit


@rate_limit(3)
async def user_test(message: Message, state: FSMContext = None):
    await message.answer('Вы начали тестирование.\n\
Вопрос №1. \n\n\
Вы часто не спите по ночам?')
    await Test.first()


async def answer_q1(message: Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data['answer1'] = answer
    await message.answer('Вопрос №2.\n\n\
Как вы себя чувствуете?')
    await Test.next()


async def answer_q2(message: Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get('answer1')
    answer2 = message.text

    await message.answer(f'Спасибо за ответы!\n\n\
Ваши ответы:\n{hcode(answer1)}\n{hcode(answer2)}')

    await state.finish()


def register_user_test(dp: Dispatcher):
    dp.register_message_handler(
        user_test, commands=["test"], chat_type=ChatType.PRIVATE)
    dp.register_message_handler(answer_q1, state=Test.Q1)
    dp.register_message_handler(answer_q2, state=Test.Q2)
