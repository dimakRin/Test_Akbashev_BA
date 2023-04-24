from create_bot import dp
from aiogram.utils import executor
from handlers.poll_handler import register_handlers_poll
from handlers.rate_handlers import register_handlers_rate
from handlers.animal_handler import register_handlers_animal
from handlers.weather_handlers import register_handlers_weather
from handlers.start_menu_handlers import register_handlers_startmenu


register_handlers_weather(dp)
register_handlers_rate(dp)
register_handlers_animal(dp)
register_handlers_poll(dp)
register_handlers_startmenu(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
