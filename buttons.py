from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

callback_data = {
    "Weather": "buttonWeather",
    "Rate": "buttonRate",
    "Animal": "buttonAnimal",
    "Poll": "buttonPoll",
    "Back": "battonBack",
    "BackA": "battonBackA"
}

# Создание кнопок главного меню
button_Weather = InlineKeyboardButton(text='Узнать погоду', callback_data=callback_data['Weather'])
button_Rate = InlineKeyboardButton(text='Конвертировать валюту', callback_data=callback_data['Rate'])
button_Animal = InlineKeyboardButton(text='Немного милоты?', callback_data=callback_data['Animal'])
button_Poll = InlineKeyboardButton(text='Создать опрос', callback_data=callback_data['Poll'])

markupStartMenu = InlineKeyboardMarkup(row_width=1).add(button_Weather, button_Rate, button_Animal, button_Poll)

#создание кнопки назад
button_back = InlineKeyboardButton(text='⬅️Назад', callback_data=callback_data['Back'])
markupBack = InlineKeyboardMarkup(row_width=1).add(button_back)
button_backA = InlineKeyboardButton(text='⬅️Назад', callback_data=callback_data['BackA'])
markupBackA = InlineKeyboardMarkup(row_width=1).add(button_backA)