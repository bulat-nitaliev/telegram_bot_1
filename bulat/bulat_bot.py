import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from static.data import greeting_text, instructions, id_passed_text
from config import TOKEN, GROUP_ID, BOT_NAME, DEV_ID
from stepic import get_stepik_token, stepik_data
from models import session, Student, Result, engine, python_for_beginner 
import keybord_bot as kb
from datetime import date
from sqlalchemy import update, insert



logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)



# @dp.inlin (lambda inline_query: True)
# async def some_inline_handler(inline_query: types.InlineQuery):
#     # создание кнопок выбора
#     keyboard = types.InlineKeyboardMarkup()
#     button1 = types.InlineKeyboardButton(text="Кнопка 1", callback_data="button1")
#     button2 = types.InlineKeyboardButton(text="Кнопка 2", callback_data="button2")
#     button3 = types.InlineKeyboardButton(text="Кнопка 3", callback_data="button3")
#     keyboard.add(button1, button2, button3)
#     chat_id = message.chat.id
#     # отправка сообщения с кнопками выбора
#     message_text = "Выберите одну из трех кнопок:"
#     message = await bot.send_message(chat_id, message_text, reply_markup=keyboard)

# функция, которая будет вызываться при нажатии на кнопки выбора
# @dp.callback_query_handler(lambda c: c.data in ["button1", "button2", "button3"])
# async def process_callback_button(callback_query: types.CallbackQuery):
#     # получение данных о нажатой кнопке
#     button_data = callback_query.data
    
#     # отправка сообщения с информацией о нажатой кнопке
#     await bot.send_message(callback_query.message.chat.id, f"Вы нажали на кнопку {button_data}")


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def welcome(message: types.Message):
    try:
        chat_id = GROUP_ID
        new_members = message.new_chat_members
        for member in new_members:
            await bot.restrict_chat_member(
                chat_id= chat_id,
                user_id= member.id,
                permissions=types.ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False
                )
            )
            user_id = member.id
            full_name = member.full_name 
            gr_msg = await bot.send_message(
                chat_id=chat_id,
                text=greeting_text % (full_name,BOT_NAME),
                parse_mode= "HTML"
            )
            photo_msg = await bot.send_photo(
                chat_id=chat_id,
                photo='static/stepik_id.jpg'
            )
            message_id = gr_msg.message_id
            await asyncio.sleep(300)
            await bot.delete_message(chat_id=chat_id,message_id=message_id)
            
    except Exception as e:
        await bot.send_message(chat_id=DEV_ID,text=e) 


@dp.message_handler(chat_type=types.ChatType.PRIVATE)
async def echo(message:types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text=instructions)
    try:
        stepik_id = int(message.text.split("/")[-1])
        user_data_url = f"https://stepik.org:443/api/users/{stepik_id}"
        stepik_token = get_stepik_token()
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

        
        
        url = 'https://stepik.org:443/api/course-grades?course=58852&user=190715002'
        data_for_beginer = stepik_data(url=url,stepik_token=stepik_token)
        for_beginner = [i for i in data_for_beginer['course-grades'][0]['results']]
        student_id = data_for_beginer['course-grades'][0]["user"]
        course_id = data_for_beginer['course-grades'][0]["course"]
        score = data_for_beginer['course-grades'][0]["score"]
        current_time = date.today()
        course_id = data_for_beginer['course-grades'][0]["course"]


        obj = Result(
            student_id = student_id,
            course_id = course_id,
            score = score,
            update_date = current_time
        )
        session.add(obj)
        session.commit()

        begin_obj = session.query(python_for_beginner).filter_by(student_id=student_id).first()
        if not begin_obj:
            insert_query = python_for_beginner.insert().values(student_id=student_id, update_date=date.today())
            session.execute(insert_query)
            session.commit()
            for key, item in data_for_beginer['course-grades'][0]["results"].items():
                if item["is_passed"]:
                    update_query = update(python_for_beginner).values(**{key: date.today()})
                    session.execute(update_query)
                    session.commit()
        else:
            for key, item in data_for_beginer['course-grades'][0]["results"].items():
                if not getattr(begin_obj, key) and data_for_beginer['course-grades'][0]["results"][key]["is_passed"]:
                    update_query = update(python_for_beginner).where(python_for_beginner.c.student_id == student_id).values(**{key: date.today()}, update_date=date.today())
                    # Выполняем запрос обновления
                    session.execute(update_query)
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
        #await message.answer('выбери кнопку', reply_markup=kb.question_kb)
        

    except Exception as e:
        await bot.send_message(chat_id=DEV_ID, text=f'{e}\n from user {tg_full_name}')



if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)
