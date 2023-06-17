import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN

"""
Создание токена бота и диспетчера + сопутствующие настройки(loop, storage).
"""

TOKEN_BOT = TOKEN

storage = MemoryStorage()
loop = asyncio.new_event_loop()
bot = Bot(token=TOKEN_BOT, parse_mode='HTML')
dp = Dispatcher(bot=bot, storage=storage, loop=loop)


if __name__ == '__main__':
    """
    Запуск бота
    """

    from handlers import dp
    executor.start_polling(dispatcher=dp)
