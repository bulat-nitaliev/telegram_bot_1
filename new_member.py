import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import TOKEN, GROUP_ID, BOT_NAME, DEV_ID
from static.data import greeting_text, id_passed_text, instructions
from stepik import stepik_data, get_stepik_token
from models import Student, session


logging.basicConfig(level=logging.INFO)
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def welcome(message: types.Message):
    try:
        chat_id = GROUP_ID
        new_members = message.new_chat_members
        for member in new_members:
            await bot.restrict_chat_member(
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
            await asyncio.sleep(5)
            greeting_msg.delete()
    except Exception as e:
        await bot.send_message(chat_id=DEV_ID, text=e)


@dp.message_handler(chat_type=types.ChatType.PRIVATE)
async def private_msgs(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text=instructions)
    try:
        stepik_id = int(message.text.split("/")[-1])
        user_data_url = f"https://stepik.org:443/api/users/{stepik_id}"
        user_data = stepik_data(user_data_url, stepik_token)
        name = user_data['users'][0]['full_name']
        tg_id = message.from_user.id
        tg_full_name = message.from_user.full_name
        new_obj = Student(
            id = stepik_id,
            name = name,
            tg_id = tg_id,
            tg_full_name = tg_full_name,
            tg_username = message.from_user.username
        )
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

    except Exception as e:
        await bot.send_message(chat_id=DEV_ID, text=f'{e}\n from user {tg_full_name}')


if __name__ == '__main__':
    stepik_token = get_stepik_token()
    executor.start_polling(dp) 
