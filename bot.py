import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from urllib.parse import urlparse
from aiogram.utils.exceptions import BadRequest
from aiogram.types import ChatPermissions
from config import TOKEN

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

logging.basicConfig(level=logging.INFO)
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['chatid'])
async def chatid(message: types.Message):
    chat_id = message.chat.id
    await message.answer(f"Ваш Chat ID: {chat_id}") 

@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: types.Message):    
    new_member_name = message.new_chat_members[0].first_name
    
    bot_username = "berenche_bot"
    bot_link = f"https://t.me/{bot_username}"
        
    welcome_message = f"Добро пожаловать в группу, {new_member_name}! Для получения инструкции напишите боту {bot_username}: {bot_link}. Первое сообщение для бота '/start' "
    await message.answer(welcome_message)
    
    try:
        await bot.restrict_chat_member(message.chat.id, message.new_chat_members[0].id, restricted_permissions)
    except BadRequest as e:
        logging.error(f"Failed to restrict user: {e}")
    
@dp.message_handler(commands = ['start'])
async def command_start(message: types.Message):
    with open("Foto.png", "rb") as file:
            await bot.send_message(message.from_user.id, "Зарегистрируйтесь на сайте {https://stepik.org} и отправьте url вашей страницы, как указано на картинке")
            await bot.send_photo(message.from_user.id, photo=file) 

@dp.message_handler() 
async def https_handler(message: types.Message):
    text = message.text
    url = urlparse(text)
    if url.scheme != 'https':
        await message.reply("Пожалуйста введите действительный HTTPS URL.")
        return
    if url.netloc != 'stepik.org':
        await message.reply("Пожалуйста введите действительный URL из сайта stepik.org")
        return
    user_id = url.path.split('/')[-1]
    await message.reply(f"Ваш ID: {user_id}. Спасибо за информацию!")
   
if __name__ == '__main__':
    executor.start_polling(dp) 

