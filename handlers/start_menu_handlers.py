from config import text
from aiogram import types
from create_bot import bot
from FSM_state import FSMWeather, FSMRate, FSMPoll
from buttons import markupStartMenu, callback_data
from aiogram.dispatcher import Dispatcher, FSMContext

#start_menu отправляет пользователю меню с функциями бота
async def start_menu(message: types.Message):
    await bot.send_message(message.from_user.id, text['StartMenu'], reply_markup=markupStartMenu)

#обработки кнопки возвращения в главное меню из машины состояний
async def back_fsm(callback: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text['StartMenu'], callback.from_user.id, callback.message.message_id,
                                reply_markup=markupStartMenu)
    await state.finish()

#обработки кнопки возвращения в главное меню
async def back(callback: types.CallbackQuery):
    await bot.edit_message_text(text['StartMenu'], callback.from_user.id, callback.message.message_id,
                                reply_markup=markupStartMenu)

#обработка сообщений не заложенных в функционал чат-бота
async def all(message: types.Message):
    await message.delete()
    await bot.send_message(message.from_user.id, text['All'], reply_markup=markupStartMenu)

def register_handlers_startmenu(dp: Dispatcher):
    dp.register_message_handler(start_menu, commands=['start'], state=None)
    dp.register_callback_query_handler(start_menu, text=callback_data['BackA'])
    dp.register_callback_query_handler(back, text=callback_data['Back'])
    dp.register_callback_query_handler(back_fsm, text=callback_data['Back'],
                                       state=[FSMWeather.weather, FSMRate.rate, FSMRate.amount, FSMPoll.poll])
    dp.register_message_handler(all)


