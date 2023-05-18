# Import the necessary modules
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
# from dotenv import load_dotenv
from os import getenv


# load_dotenv()
# BOT_TOKEN = getenv('TestPurposes123Bot')

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create a bot instance
bot = Bot(token='5504422051:AAHSqYQBHRUFmyUZi0iFX7AG-cIw7HI1fvo')

# Create a dispatcher instance
dp = Dispatcher(bot)

# Define a message handler that echoes back messages
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

# Start the bot using the executor
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
