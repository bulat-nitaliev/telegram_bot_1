import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['chatid'])
async def chatid(message: types.Message):
    chat_id = message.chat.id
    await message.answer(f"Ваш Chat ID: {chat_id}")







if __name__ == '__main__':
    executor.start_polling(dp) 
