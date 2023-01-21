# # # # # # # # # # # # # # # # # # # # # # # # # #
#                     Title                       #
#              Clicker telegram bot               #
#                                                 #
#                  Description                    #
#        Телеграм бот написанный на aiogram       #
#                                                 #
#             Команды: /start, /top               #
#                by - tg: @exyled                 #
# # # # # # # # # # # # # # # # # # # # # # # # # #

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN # Токен бота
import logging
from time import strftime

# aiogram
bot = Bot(token=TOKEN) # Токен бота
dp = Dispatcher(bot=bot)

# Игра
clicks = 0
users = {}

# Logging
logging.basicConfig(level=logging.INFO, filename=f"bot.log",filemode="w", encoding="utf-8")

welcome_message = "Привет, Нажимай конпку и стоновись лучше 🙈\nКол-во кликов - {}"

# Создание топа участников
def generate_top() -> list:
    top_list = []
    if users:
        for user in users:
            top_list.append((user, users[user]["clicks"]))
        sorted_top = sorted(top_list, key=lambda item: item[1])
        sorted_top.reverse()
        top = ""
        top = "Топ участников:\n"
        for user in sorted_top:
            top = top + f"  {user[0]} - {user[1]}\n"
    else:
        top = "В топе пока нет участников\nТы можешь стать первым😉"
    return top

# Создание кнопки нажатия
def generate_click_button() -> InlineKeyboardMarkup:
    keyboard_markup = types.InlineKeyboardMarkup()
    keyboard_markup.add(
        InlineKeyboardButton('Клик', callback_data="click"),
    )
    return keyboard_markup

# Создание кнопки обновления топа
def generate_update_top_button() -> InlineKeyboardMarkup:
    keyboard_markup = types.InlineKeyboardMarkup()
    keyboard_markup.add(
        InlineKeyboardButton('Обновить', callback_data="update"),
    )
    return keyboard_markup

# Добавление пользователя
def add_user(tag, id, full_name) -> dict:
    global users
    users[tag] = {
        "id" : id,
        "full_name" : full_name,
        "clicks" : 1
    }
    time = strftime("%H:%M")
    logging.info(f"{time} - {tag} : {users[tag]}")

# Команда /start
@dp.message_handler(commands='start')
async def welcome(message: types.Message):
    tag = message.chat.username
    id = message.chat.id
    full_name = message.chat.full_name
    if not tag in users:
        add_user(tag, id, full_name)
    await bot.send_message(
        chat_id=message.chat.id,
        text=welcome_message.format(clicks),
        reply_markup=generate_click_button()
    )

@dp.message_handler(commands=["top"])
async def sand_top(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=generate_top(),
        reply_markup=generate_update_top_button()
    )

@dp.callback_query_handler(text="update")
@dp.callback_query_handler(text="click")
async def callback_handler(query: types.CallbackQuery):
    global clicks, users
    tag = query.message.chat.username
    if query.data == "click":
        clicks += 1
        users[tag]["clicks"] += 1
        await bot.edit_message_text(
            text=welcome_message.format(clicks),
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            reply_markup=generate_click_button()
        )
    elif query.data == "update":
        if not query.message.text is generate_top():
            await bot.edit_message_text(
                text=generate_top(),
                chat_id=query.message.chat.id,
                message_id=query.message.message_id,
                reply_markup=generate_update_top_button()
            )

def main():
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()