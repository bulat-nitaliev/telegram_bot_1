import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import TOKEN


logging.basicConfig(level=logging.INFO)
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)


# Приветствие новых пользователей
@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def greet_new_members(message: types.Message):
    for user in message.new_chat_members:
        user_id = user.id
        welcome_message = "Добро пожаловать в нашу образовательную группу! Мы здесь изучаем Python\U0001F40D\nНаша " \
                        "цель это достижение результата посредством взаимопомощи в процессе обучения.\nДля того " \
                        "чтобы стать частью нашего дружного коллектива, пожалуйста, напишите нашему боту сообщение " \
                        "'/start' для получения дальнейших инструкций:\n@shibzuko_training1_bot\n\n" \
                        "P.S. Этого бота разработали участники нашего сообщества :)"
        message_to_admin = f"В группу А присоединился новый пользователь"
        await bot.send_message(GROUP_ID, welcome_message)
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            permissions=types.ChatPermissions(can_send_messages=False)
        )


# Отправка инструкции пользователю припервом запуске бота или по команде /start
@dp.message_handler(commands='start', chat_type=types.ChatType.PRIVATE)
async def instruction(message: types.Message):
    chat_id = message.chat.id
    photo_path = "media/stepik.png"
    text = (f'Welcome!\nНаша цель - это создание сплоченного коллектива в котором все будут помогать и '
                        f'мотивировать друг друга.\n\nОсновной площадкой нашего обучения является платформа '
                        f'https://stepik.org, а в частности линейка из серии курсов "Поколение Python", в которую входят:\n\n'
                         f'"Поколение Python": курс для начинающих - https://stepik.org/course/58852\n\n'
                         f'"Поколение Python": курс для продвинутых - https://stepik.org/course/58852\n\n'
                         f'"Поколение Python": курс для профессионалов - https://stepik.org/course/58852\n'
                         f'и другие.\n\n'
                         f'Для того чтобы обучение проходило эффективно и под контролем наставников'
                         f', мы разработали бота который будет собирать данные о прохождении вами курсов. '
                         f'Для этого вам небходимо: \n\n'
                         f'1. Перейти по ссылке(открыть в браузере) https://stepik.org и '
                         f'зарегистрироваться(авторизоваться, если вы уже зарегистрированы)\n'
                         f'2. Перейти в "Профиль" в верхнем правом углу\n'
                         f'3. Скопировать URL-адрес из адресной строки(пример:https://stepik.org/users/315844473) '
                         f'и отправить мне')
    await bot.send_photo(chat_id, photo=open(photo_path, 'rb'), caption=text)


# Проверка URL пользователя
@dp.message_handler(chat_type=types.ChatType.PRIVATE)
async def test_url(message: types.Message, can_send_messages=False):
    user_id = message.from_user.id
    username = message.chat.username
    text = message.text
    group_link = f"https://t.me/joinchat/{GROUP_ID}"

    if 'https://stepik.org/users/' in text and text[text.rfind('/')+1:].isdigit():
        await bot.send_message(GROUP_ID, f'Благодарю за информацию! Добро пожаловать! '
                                        f'Теперь вы можете отправлять сообщения в группе {group_link}')
        if can_send_messages is False:
            await bot.restrict_chat_member(
                chat_id=GROUP_ID,
                user_id=user_id,
                permissions=types.ChatPermissions(can_send_messages=True)
            )
        await bot.send_message(ADMIN, f'Пользователь @{username} добавил stepik_id:{text}. Проверьте корректность данных')
    else:
        await message.answer('Пожалуйста, введите корректный URL-адрес\nПример: https://stepik.org/users/315844473')


if __name__ == '__main__':
    executor.start_polling(dp) 
