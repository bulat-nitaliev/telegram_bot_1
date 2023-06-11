import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import TOKEN, GROUP_ID, BOT_NAME, DEV_ID
from static.data import greeting_text, id_passed_text, instructions, step_course_advance, step_course_beginner
from stepik import stepik_data, get_stepik_token, html_title
from models import Student, Result, session, python_for_beginner, python_for_advanced, StepNameForBeginners, StepNameForAdvances
from datetime import date

logging.basicConfig(level=logging.INFO)
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

update_date = date.today()

course_number = {58852: python_for_beginner,68343: python_for_advanced}


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
    
    result_data_url =f'https://stepik.org:443/api/course-grades?user={stepik_id}'
    result_data = stepik_data(result_data_url, stepik_token)
    
    for i in range(len(result_data['course-grades'])):
                          
        course_id = result_data['course-grades'][i]['course']
        score = result_data['course-grades'][i]['score']
        update_date = date.today()
                
        # проверяем, есть ли уже такая запись в базе данных
        existing_record = session.query(Result).filter_by(student_id=stepik_id, course_id=course_id).first()

        if existing_record:
            
            existing_record.score = score
            existing_record.update_date = update_date
            
        else:
            new_record = Result(student_id=stepik_id, course_id=course_id, score=score, update_date=update_date)
            session.add(new_record)  

        # сохраняем изменения в базе данных
        session.commit()  
      
    session.merge(new_obj)
    session.commit()
    
    for course, table in course_number.items():
        
        course_number1 = f'https://stepik.org:443/api/course-grades?course={course}&user={stepik_id}'
        
        begin_data = stepik_data(course_number1, stepik_token)
        
        for key, i in begin_data['course-grades'][0]['results'].items():
            if i['is_passed']:
                record = session.query(table).filter_by(student_id=stepik_id).first()

                if record:
                    if getattr(record, key) is None:
                        session.execute(table.update().values(**{key: update_date}).where(table.c.student_id == stepik_id))
                else:
                    ins = table.insert().values(student_id=stepik_id, update_date=update_date, **{key: update_date})
                    session.execute(ins)

                session.commit()
            else:
                continue
               
    step_course_all = {StepNameForBeginners: step_course_beginner, StepNameForAdvances: step_course_advance}
    
    for table_course, step_cours in step_course_all.items():
        for name_step in step_cours:
            record = session.query(table_course).filter_by(id=name_step).first()
            
            if record:
                continue
            else:
                step_title_url = f'https://stepik.org/lesson/{name_step}/step/1?unit=406701'
                txt = html_title(step_title_url)            
                new_step = table_course(id=name_step, name=txt[:txt.find('—')])                      
                session.add(new_step)
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

if __name__ == '__main__':
    stepik_token = get_stepik_token()
    executor.start_polling(dp) 
