from config import text
from aiogram import types
from create_bot import bot
from FSM_state import FSMPoll
from aiogram.dispatcher import Dispatcher, FSMContext
from buttons import callback_data, markupBack


# функция формирования сообщения в ответ на нажатие кнопки:"Создать опрос"
async def callback_poll(callback: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text['CallbackPoll'],callback.from_user.id,callback.message.message_id,
                                 reply_markup=markupBack)
    await callback.answer()
    async with state.proxy() as data:
        data['id'] = callback.message.message_id # запись id сообщения для коректного корректирования
    await FSMPoll.poll.set()


async def answer_poll(message: types.Message, state: FSMContext):
    poll = message.poll
    if poll: # проверка на то что прислали опрос
        options = []
        for op in poll['options']: # Запись вариантов ответов
            options.append(op['text'])
        try:
            await bot.send_poll(-942965153, question=poll['question'], options=options)
            async with state.proxy() as data:
                await bot.edit_message_text(text['AnswerPoll'], message.from_user.id, data['id'],
                                            reply_markup=markupBack)
        except: # Исключение на случай если будет не правильно введен id группы
            async with state.proxy() as data:
                await bot.edit_message_text(text['AnswerPollId'], message.from_user.id, data['id'],
                                            reply_markup=markupBack)
        await message.delete()
        await state.finish()
    else: # В случае, если отправили обычные сообщения
        await message.delete()
        async with state.proxy() as data:
            try:
                await bot.edit_message_text(text['AnswerPollAll'], message.from_user.id, data['id'],
                                            reply_markup=markupBack)
            except:
                pass


def register_handlers_poll(dp: Dispatcher):
    dp.register_callback_query_handler(callback_poll, text=callback_data['Poll'])
    dp.register_message_handler(answer_poll, content_types=['poll'], state=FSMPoll.poll)
    dp.register_message_handler(answer_poll, state=FSMPoll.poll)