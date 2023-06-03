import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from urllib.parse import urlparse
from aiogram.types import ChatPermissions
from config import TOKEN, CHAT_ID
from models import Student, Session
from stepik import html_title


logging.basicConfig(level=logging.INFO)
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: types.Message): 
       
    new_member_name = message.new_chat_members[0].first_name
    
    bot_username = "berenche_bot"
    bot_link = f"https://t.me/{bot_username}"
        
    welcome_message = f"Добро пожаловать в группу, {new_member_name}!"\
                      f"Для получения инструкции напишите боту {bot_username}: {bot_link}. Первое сообщение для бота '/start' "
    await message.answer(welcome_message)
    restricted_permissions = ChatPermissions( 
        can_send_messages=False, 
        can_send_media_messages=False, 
        can_send_polls=False, 
        can_send_other_messages=False, 
        can_add_web_page_previews=False, 
        can_change_info=False, 
        can_invite_users=False, 
        can_pin_messages=False 
    )     
     
    await bot.restrict_chat_member(message.chat.id, message.new_chat_members[0].id, restricted_permissions) 
    
    
@dp.message_handler(commands = ['start'],chat_type=types.ChatType.PRIVATE)
async def command_start(message: types.Message):
    with open("Foto.png", "rb") as file:
            await bot.send_message(message.from_user.id,
                "Зарегистрируйтесь на сайте {https://stepik.org} и отправьте url вашей страницы, как указано на картинке")
            await bot.send_photo(message.from_user.id, photo=file) 
            

@dp.message_handler(content_types=[types.ContentType.TEXT],chat_type=types.ChatType.PRIVATE)
async def process(message: types.Message): 
             
    text = message.text
    url = urlparse(text)
    if url.scheme != 'https':
        await message.reply("Введите пожалуйста действительный URL")
        return
    if url.netloc != 'stepik.org':
        await message.reply("Введите пожалуйста действительный URL согласно инструкции")
        return
    user_id = url.path.split('/')[-1]
    
    if user_id.isdigit():        
        unrestricted_permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True
            )
        await bot.restrict_chat_member(CHAT_ID, message.from_user.id, unrestricted_permissions)
        await message.reply(f"Ваш ID: {user_id}. Спасибо за информацию!"
                        f" Теперь вам открыт доступ к главной группе.")
        
        session = Session()
        url = f"https://stepik.org/users/{user_id}"
        name = html_title(url)
        student = Student(name = name,tg_id=message.from_user.id, tg_full_name=message.from_user.first_name, tg_username=message.from_user.username)
        session.add(student)
        session.commit()
        
        await message.reply("Теперь Вы внесены в базу студентов.")       
       
    else:
        await message.reply("Введите пожалуйста действительный URL. В ID могут быть только цифры!")
   
if __name__ == '__main__':
    executor.start_polling(dp) 

