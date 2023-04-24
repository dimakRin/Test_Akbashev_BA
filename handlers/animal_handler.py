import random
from config import text
from aiogram import types
from create_bot import bot
from aiogram.dispatcher import Dispatcher
from buttons import callback_data, markupBackA


#Функция отправляет пользователю рандомную картинку
async def callback_animal(callback: types.CallbackQuery):
    rand = int(random.random()*5)+1 # создает рандомное целое число от 1 до 5
    await callback.message.delete()
    with open('imgs/{}.jpg'.format(rand), 'rb') as photo:# загрузка картинки
        await bot.send_photo(chat_id=callback.from_user.id,
                                 photo=photo, caption=text['CallbackAnimal'], reply_markup=markupBackA)

    await callback.answer()


def register_handlers_animal(dp: Dispatcher):
    dp.register_callback_query_handler(callback_animal, text=callback_data['Animal'])