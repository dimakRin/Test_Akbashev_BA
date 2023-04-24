from config import text
from aiogram import types
from create_bot import bot
from api import get_weather_info
from FSM_state import FSMWeather
from aiogram.dispatcher import Dispatcher, FSMContext
from buttons import callback_data, markupBack


# функция формирования сообщения в ответ на нажатие кнопки:"Узнать погоду"
async def callback_weather(callback: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text( text['CallbackWeather'],callback.from_user.id,callback.message.message_id,
                                 reply_markup=markupBack)
    await callback.answer()
    async with state.proxy() as data:
        data['id'] = callback.message.message_id # запись id сообщения для коректного корректирования
    await FSMWeather.weather.set()               # запуск состояния ожидания ответа о городе

# функция формирующая ответ на отправленый пользователем город
async def answer_weather(message: types.Message, state: FSMContext):
    data_w = get_weather_info(message.text)  # получение данных о погоде в городе в виде словаря
    if data_w:
        async with state.proxy() as data:
            await bot.edit_message_text(text['AnswerWeatherT']
                                   .format(data_w['city'], data_w['temp'],data_w['wind']),
                                        message.from_user.id,data['id'], reply_markup=markupBack)
        await message.delete()
        await state.finish()
    else:
        # ответ в случае неккоректного ввода города
        async with state.proxy() as data:
            try:
                await bot.edit_message_text(text['AnswerWeatherF'], message.from_user.id, data['id'], reply_markup=markupBack)
            except:
                pass
        await message.delete()





def register_handlers_weather(dp: Dispatcher):
    dp.register_callback_query_handler(callback_weather, text=callback_data['Weather'])
    dp.register_message_handler(answer_weather, state=FSMWeather.weather)