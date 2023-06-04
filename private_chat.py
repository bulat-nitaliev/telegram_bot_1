import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import TOKEN, GROUP_ID, BOT_NAME, DEV_ID
from static.data import greeting_text, instructions
from stepik import stepik_data, get_stepik_token
from models import Student, session

logging.basicConfig(level=logging.INFO)
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)





# @dp.message_handler(commands='start', chat_type=types.ChatType.PRIVATE)
# async def instruction(message: types.Message):
#     print(message)



# @dp.message_handler(commands='start', chat_type=types.ChatType.PRIVATE)
# async def instruction(message: types.Message):
#     chat_id = message.chat.id
#     await bot.send_message(chat_id=chat_id, text=instructions)
#     with open('static/stepik_id.jpg', 'rb') as photo:
#         await bot.send_photo(chat_id=chat_id, photo=photo)
#     # show message_handler
#     # get stepik id


# @dp.message_handler(chat_type=types.ChatType.PRIVATE)
# async def instruction(message: types.Message):
#     try:
#         stepik_id = int(message.text.split("/")[-1])
#     except Exception as e:
#         await bot.send_message(chat_id=DEV_ID, text=e)
#     # check stepik_id, add to db



@dp.message_handler(chat_type=types.ChatType.PRIVATE)
async def instruction(message: types.Message):
    try:
        stepik_id = int(message.text.split("/")[-1])
        user_data_url = f"https://stepik.org:443/api/users/{stepik_id}"
        user_data = stepik_data(user_data_url, stepik_token)
        name = user_data['users'][0]['full_name']
        new_obj = Student(
            id = stepik_id,
            name = name,
            tg_id = message.from_user.id,
            tg_full_name = message.from_user.full_name,
            tg_username = message.from_user.username
        )
        session.merge(new_obj)
        session.commit()

    except Exception as e:
        await bot.send_message(chat_id=DEV_ID, text=e)
    # add details to dev msg

if __name__ == '__main__':
    stepik_token = get_stepik_token()
    executor.start_polling(dp) 