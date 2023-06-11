from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bt_question = KeyboardButton("Задать вопрос")
bt_literature = KeyboardButton("Литература")
bt_motivation = KeyboardButton("Мотивация")
question_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(bt_question).add(bt_motivation).insert(bt_literature)