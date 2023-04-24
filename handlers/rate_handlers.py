from config import text
from aiogram import types
from create_bot import bot
from FSM_state import FSMRate
from api import get_rate_info
from transliterate import translit
from aiogram.dispatcher import Dispatcher,FSMContext
from buttons import callback_data, markupBack, markupStartMenu


# функция формирования сообщения в ответ на нажатие кнопки:"Конвертировать валюты"
async def callback_rate(callback: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text['CallbackRate'], callback.from_user.id, callback.message.message_id,
                                 reply_markup=markupBack)
    await callback.answer()
    async with state.proxy() as data:
        data['id'] = callback.message.message_id # запись id сообщения для коректного корректирования
    await FSMRate.rate.set()


#функцию обрабатывающая запись пары конвертируемых валют
async def rate_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if '/' in message.text:  # Проверка на наличие разделителя в сообщении
            await bot.edit_message_text(text['AnswerRateT'], message.from_user.id, data['id'],
                                        reply_markup=markupBack)
            data['rate'] = translit(message.text, language_code='ru', reversed=True)# Запись пары валют
            await FSMRate.amount.set()                                              # Установка следующего состояния
        else:
            await bot.edit_message_text(text['AnswerRateF'], message.from_user.id, data['id'],
                                        reply_markup=markupBack) # Сообщение: нет разделителя /
    await message.delete()

#функцию обрабатывающая прием суммы и конвертацию валют
async def amount_answer(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        if message.text.isdigit():# проверка, что в качестве суммы - ввели число
            rate = data['rate'].split('/')

            data_r = get_rate_info(rate[0].upper(), rate[1].upper(), message.text)#получаем словарь с данными о конвертации
            if data_r['status'] == 'success': # Формуриется сообщение с результатом конвертации
                await bot.edit_message_text(text['AnswerAmountS']
                                            .format(data_r['amount'], data_r['from'], data_r['result'], data_r['to'])
                                            , message.from_user.id, data['id'], reply_markup=markupBack)
                await state.finish()
            elif data_r['status'] == 'to_error':# Формуриется сообщение об ошибке первой валюты
                await bot.edit_message_text(text['AnswerAmountEt'], message.from_user.id, data['id'],
                                            reply_markup=markupBack)
                await FSMRate.rate.set()
            elif data_r['status'] == 'from_error':# Формуриется сообщение об ошибке второй валюты
                await bot.edit_message_text(text['AnswerAmountEf'], message.from_user.id, data['id'],
                                            reply_markup=markupBack)
                await FSMRate.rate.set()
            elif data_r['status'] == 'amount_error':
                await bot.edit_message_text(text['AnswerAmountE'], message.from_user.id, data['id'],
                                            reply_markup=markupBack)
            elif data_r['status'] == 'connect_error':
                await bot.edit_message_text(text['AnswerAmountC'], message.from_user.id, data['id'],
                                            reply_markup=markupStartMenu)
                await state.finish()
        else:
            await bot.edit_message_text(text['AnswerAmountE'], message.from_user.id, data['id'],
                                        reply_markup=markupBack)




def register_handlers_rate(dp: Dispatcher):
    dp.register_callback_query_handler(callback_rate, text=callback_data['Rate'])
    dp.register_message_handler(rate_answer, state=FSMRate.rate)
    dp.register_message_handler(amount_answer, state=FSMRate.amount)