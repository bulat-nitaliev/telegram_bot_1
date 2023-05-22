# Import the necessary modules
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import TOKEN

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create a bot instance
bot = Bot(token=TOKEN)

# Create a dispatcher instance
dp = Dispatcher(bot)

# Command handler for /chatid
@dp.message_handler(commands=['chatid'])
async def chatid(message: types.Message):
    chat_id = message.chat.id
    await message.answer(f"Ваш Chat ID: {chat_id}")

# Define a message handler that echoes back messages
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


# Start the bot using the executor
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
