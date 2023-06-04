import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import TOKEN, GROUP_ID, BOT_NAME
from static.data import greeting_msg

logging.basicConfig(level=logging.INFO)
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)




# new chat member
# @dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
# async def welcome(message: types.Message):
#     print(message)


# restrict
# @dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
# async def welcome(message: types.Message):
#     chat_id = 
#     user_id = 
#     # show restrict_chat_member
#     await bot.restrict_chat_member(
#         chat_id=,
#         user_id=,
#         permissions=types.ChatPermissions(can_send_messages=False, can_send_media_messages=False)
#     )


# send msg
# @dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
# async def welcome(message: types.Message):
#     chat_id = GROUP_ID
#     new_members = message.new_chat_members
#     for member in new_members:
#         await bot.restrict_chat_member(
#             chat_id=chat_id,
#             user_id=member.id,
#             permissions=types.ChatPermissions(can_send_messages=False, can_send_media_messages=False)
#         )

#         # show send_msg
#         await bot.send_message(chat_id=, text=)


# @dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
# async def welcome(message: types.Message):
#     chat_id = GROUP_ID
#     new_members = message.new_chat_members
#     for member in new_members:
#         await bot.restrict_chat_member(
#             chat_id=chat_id,
#             user_id=member.id,
#             permissions=types.ChatPermissions(can_send_messages=False, can_send_media_messages=False)
#         )

#         await bot.send_message(chat_id=chat_id, text=greeting_msg % (member.full_name, BOT_NAME))



if __name__ == '__main__':
    executor.start_polling(dp) 
