# Import the necessary modules
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from stepik import get_stepik_token, stepik_data
from config import TOKEN

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create a bot instance
bot = Bot(token = TOKEN)

# Create a dispatcher instance 
dp = Dispatcher(bot)

# Define a message handler that echoes back messages
@dp.message_handler(commands=['chatid'])
async def chatid(message: types.Message):
    chat_id = message.chat.id
    await message.answer(f"Ваш Chat ID: {chat_id}")


@dp.message_handler(commands=['stat'])
async def chatid(message: types.Message):
    data = stepik_data("https://stepik.org:443/api/course-grades?course=68343&user=270531229", stepik_token)
    await message.answer(data)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

# Start the bot using the executor
if __name__ == '__main__':
    stepik_token = get_stepik_token()
    executor.start_polling(dp) 
