import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import TOKEN, tg_grupp, tg_bot, DEV_ID


logging.basicConfig(level=logging.INFO)
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)


# Приветствие новых пользователей
@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def welcome(message: types.Message):
    global new_member, chat_id_group
    new_member = message.new_chat_members
    new_name = message.new_chat_members[0]['first_name']
    chat_id_group = message.chat.id
    welcome_message =f"{new_name} \nДобро пожаловать в нашу образовательную группу! Мы здесь изучаем Python\U0001F40D\nНаша " \
                      "цель это достижение результата посредством взаимопомощи в процессе обучения.\nДля того " \
                      "чтобы стать частью нашего дружного коллектива, пожалуйста, напишите нашему боту сообщение " \
                     f"'/start' для получения дальнейших инструкций:\n  {tg_bot} \n\n" \
                      "P.S. Этого бота разработали участники нашего сообщества :)"
    message_to_admin = f"В группу присоединился новый пользователь {new_member}"
    await bot.send_message(chat_id_group, welcome_message)
    await bot.send_message(DEV_ID, message_to_admin)
    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=new_member[0].id,
        permissions=types.ChatPermissions(can_send_messages=False)
    )


# Отправка инструкции пользователю припервом запуске бота или по команде /start
@dp.message_handler(commands='start', chat_type=types.ChatType.PRIVATE)
async def instruction(message: types.Message):
    chat_id = message.chat.id
    photo_path = r'C:\Users\6417\Desktop\Bot\telegram_bot_1\png\stepic.png'
    description = 'URL-адрес из адресной строки'
    photo_path = "media/stepik.png"
# Проверка URL пользователя
    if 'https://stepik.org/users/' in text and text[text.rfind('/')+1:].isdigit():
        await bot.send_message(chat_id, f'Благодарю за информацию! Добро пожаловать! '
                                        f'Теперь вы можете отправлять сообщения в группе {tg_grupp}')
        dic[chat_id] = [username,text]
        await bot.send_message(DEV_ID, f'словарь {dic}')
    group_link = f"https://t.me/joinchat/{GROUP_ID}"

    if 'https://stepik.org/users/' in text and text[text.rfind('/')+1:].isdigit():
        await bot.send_message(GROUP_ID, f'Благодарю за информацию! Добро пожаловать! '
                                        f'Теперь вы можете отправлять сообщения в группе {group_link}')
        await bot.send_message(DEV_ID, f'Пользователь @{username} добавил stepik_id:{text}. Проверьте корректность данных')
    else:
        await message.answer('Пожалуйста, введите корректный URL-адрес\nПример: https://stepik.org/users/315844473')
    await message.answer(f"Ваш Chat ID: {chat_id}") 


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

