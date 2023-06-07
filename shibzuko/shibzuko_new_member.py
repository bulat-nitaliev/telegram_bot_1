import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from shibzuko.config import TOKEN, GROUP_ID, BOT_NAME, DEV_ID, GROUP_NAME, ADMIN
from shibzuko.static.data import greeting_text, id_passed_text, instructions, message_for_admin, url_error
from shibzuko.stepik import stepik_data, get_stepik_token
from shibzuko.models import Student, session

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)  # Ловит новых пользователей
async def welcome(message: types.Message):
    chat_id = GROUP_ID
    new_members = message.new_chat_members
    for member in new_members:
        await bot.restrict_chat_member(  # Блокирует возможность отправки сообщений в чат
            chat_id=chat_id,
            user_id=member.id,
            permissions=types.ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False
            )
        )
        greeting_msg = await bot.send_message(
            chat_id=chat_id,
            text=greeting_text % (member.full_name, BOT_NAME)
        )
        await asyncio.sleep(300)
        await greeting_msg.delete()


# Отправка инструкции пользователю при первом запуске бота или по команде /start
@dp.message_handler(commands='start', chat_type=types.ChatType.PRIVATE)
async def instruction(message: types.Message):
    chat_id = message.chat.id
    photo_path = "static/stepik_id.jpg"
    text = instructions
    await bot.send_photo(chat_id, photo=open(photo_path, 'rb'), caption=text)


# Проверка URL пользователя
@dp.message_handler(chat_type=types.ChatType.PRIVATE)
async def test_url(message: types.Message, can_send_messages=False):
    group_name = GROUP_NAME
    user_id = message.chat.id
    username = message.chat.username
    text = message.text
    stepik_id = text.split('/')[-1]
    if 'https://stepik.org/users/' in text and stepik_id.isdigit():
        await bot.send_message(user_id, id_passed_text % (group_name))
        if can_send_messages is False and user_id is not ADMIN:
            await bot.restrict_chat_member(
                chat_id=GROUP_ID,
                user_id=user_id,
                permissions=types.ChatPermissions(can_send_messages=True)
            )
        await bot.send_message(ADMIN, message_for_admin % (username, text))

        #############################

        user_data_url = f"https://stepik.org:443/api/users/{stepik_id}"
        user_data = stepik_data(user_data_url, stepik_token)
        name = user_data['users'][0]['full_name']
        tg_id = message.from_user.id
        tg_full_name = message.from_user.full_name
        new_obj = Student(
            id=stepik_id,
            name=name,
            tg_id=tg_id,
            tg_full_name=tg_full_name,
            tg_username=message.from_user.username
        )
        print()
        session.merge(new_obj)
        session.commit()
        await bot.restrict_chat_member(
            chat_id=GROUP_ID,
            user_id=tg_id,
            permissions=types.ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True
            )
        )
        invite_link = await bot.export_chat_invite_link(GROUP_ID)
        await message.answer(text=id_passed_text % invite_link)

        #############################


    else:
        await bot.send_message(user_id, url_error)


# @dp.message_handler(chat_type=types.ChatType.PRIVATE)
# async def private_msgs(message: types.Message):
#     chat_id = message.chat.id
#     await bot.send_message(chat_id=chat_id, text=instructions)
#
#     stepik_id = int(message.text.split("/")[-1])
#     user_data_url = f"https://stepik.org:443/api/users/{stepik_id}"
#     user_data = stepik_data(user_data_url, stepik_token)
#     name = user_data['users'][0]['full_name']
#     tg_id = message.from_user.id
#     tg_full_name = message.from_user.full_name
#     new_obj = Student(
#         id = stepik_id,
#         name = name,
#         tg_id = tg_id,
#         tg_full_name = tg_full_name,
#         tg_username = message.from_user.username
#     )
#     session.merge(new_obj)
#     session.commit()
#     await bot.restrict_chat_member(
#         chat_id=GROUP_ID,
#         user_id=tg_id,
#         permissions=types.ChatPermissions(
#             can_send_messages=True,
#             can_send_media_messages=True
#         )
#     )
#     invite_link = await bot.export_chat_invite_link(GROUP_ID)
#     await message.answer(text=id_passed_text % invite_link)


if __name__ == '__main__':
    stepik_token = get_stepik_token()
    executor.start_polling(dp)
