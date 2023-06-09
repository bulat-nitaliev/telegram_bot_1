import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import TOKEN, BOT_NAME, GROUP_ID
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import ChatTypeFilter, IsReplyFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

logging.basicConfig(level=logging.INFO)
bot = Bot(token = TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['chatid'])
async def chatid(message: types.Message):
    chat_id = message.chat.id
    await message.answer(f"Ваш Chat ID: {chat_id}")


# Здесь будет ваш код

# Обработчик вступления новых участников
# Определение состояния для ожидания правильного степик URL от участника
class RegistrationState(StatesGroup):
    WaitingForURL = State()

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member_join(message: types.Message):
    for new_member in message.new_chat_members:
        new_member_name = new_member.first_name
        new_member_id = new_member.id


        # Ограничение прав нового участника на отправку сообщений
        permissions = types.ChatPermissions(can_send_messages=False)
        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=new_member_id, permissions=permissions)

        # Отправка приветственного сообщения в группу
        welcome_message = f"Привет, {new_member_name}! Мы здесь учим Python и помогаем друг другу. Напиши мне {BOT_NAME}, чтобы продолжить."
        await bot.send_message(chat_id=GROUP_ID, text=welcome_message)

# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message, state: FSMContext):
    # Отправка инструкции и фото
    photos = [
    types.InputMediaPhoto(media=open('media/photo1.png', 'rb'), caption='Step 1 - Нажимаем на иконку в правом верхнем углу.'),
    types.InputMediaPhoto(media=open('media/photo2.png', 'rb'), caption='Step 2 - Нажимаем на "Profile"'),
    types.InputMediaPhoto(media=open('media/photo3.png', 'rb'), caption='Step 3 - Нажимаем на строку запроса'),
    types.InputMediaPhoto(media=open('media/photo4.png', 'rb'), caption='Step 4 - Копируем и отправляем боту URL'),
]
    await bot.send_message(chat_id=message.chat.id, text="Добро пожаловать! Пожалуйста, отправьте ваш URL как показано на следующих фотографиях.")
    await message.reply_media_group(media=photos)

    
    # Установка состояния ожидания степик URL для данного участника
    # # Получаем информацию о пользователе
    tg_user = message.from_user
    tg_id = tg_user.id
    # tg_first_name = tg_user.first_name  # Имя пользователя
    # tg_last_name = tg_user.last_name    # Фамилия пользователя (может быть None)
    # tg_username = tg_user.username      # Юзернейм пользователя (может быть None)
    # if last_name:
    #     full_name = f"{first_name} {last_name}"
    # else:
    #     full_name = first_name

    await RegistrationState.WaitingForURL.set()
    await state.update_data(member_id=tg_id)


# Обработчик текстовых сообщений
@dp.message_handler(state=RegistrationState.WaitingForURL, content_types=types.ContentTypes.TEXT)
async def handle_url_message(message: types.Message, state: FSMContext):
    # Обработка полученного степик URL
    stepik_url = message.text

    # Проверка правильности степик URL 

    if stepik_url.startswith("https://stepik.org/users/"):
        # Разрешение участнику отправлять сообщения в группе
        data = await state.get_data()
        member_id = data.get("member_id")
        permissions = types.ChatPermissions(can_send_messages=True)
        await bot.restrict_chat_member(chat_id=GROUP_ID, user_id=member_id, permissions=permissions)

        # Извлечение степик айди из URL
        stepik_id = message.text.split("/")[-1]

        # Дальнейшая обработка степик айди
        await message.reply(f"Степик айди: {stepik_id}")

        # Отправка подтверждения о разрешении отправки сообщений
        confirmation_message = "Спасибо! Вы можете теперь отправлять сообщения в группе."
        await message.reply(confirmation_message)

        # Сброс состояния участника
        await state.finish()
    else:
        # Обработка неправильного степик URL
        error_message = "Неправильный формат URL. Пожалуйста, отправьте URL, начинающийся с 'https://stepik.org/users/'."
        await message.reply(error_message)




if __name__ == '__main__':
    executor.start_polling(dp) 
