# Import the necessary modules
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create a bot instance
bot = Bot(token='6119724113:AAGI1J30EvUHUv8cND0b7S_LR-94JXMi_F8')

# Create a dispatcher instance
dp = Dispatcher(bot)

# Define a message handler that echoes back messages
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

# Start the bot using the executor
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
