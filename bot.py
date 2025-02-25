import random
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

# Token
TOKEN = "8059081878:AAFYJBDijfhgBKtW4ictU5NXDH5WFXeRnRY"

# Bot and Dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# User storage
waiting_users = []
active_chats = {}

# Keyboard
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔍 Найти тень")],
        [KeyboardButton(text="📜 Кодекс теней")],
        [KeyboardButton(text="🛑 Оборвать связь")]
    ],
    resize_keyboard=True
)

# Responses
find_shadow_responses = [
    "✅ Тень найдена! Начинайте общение.",
    "✅ Ты встретил свою тень. Приятного общения.",
    "✅ Тень рядом. Начинай разговор."
]

# Command /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Добро пожаловать в элитное общество теней! Нажмите '🔍 Найти тень', чтобы начать.", reply_markup=keyboard)

# Find a shadow
@dp.message(lambda message: message.text == "🔍 Найти тень")
async def find_chat(message: types.Message):
    user_id = message.from_user.id

    if user_id in active_chats:
        await message.answer("❌ Ты говоришь с тенью!")
        return

    if waiting_users and waiting_users[0] != user_id:
        partner_id = waiting_users.pop(0)
        active_chats[user_id] = partner_id
        active_chats[partner_id] = user_id

        await bot.send_message(partner_id, "✅ Тень найдена! Начинайте общение.")
        response = random.choice(find_shadow_responses)
        await message.answer(response)
    else:
        if user_id not in waiting_users:
            waiting_users.append(user_id)
        await message.answer("⏳ В поисках тени...")

# Stop chat /stop command
@dp.message(Command("stop"))
async def stop_chat(message: types.Message):
    user_id = message.from_user.id

    if user_id in active_chats:
        partner_id = active_chats.pop(user_id)
        active_chats.pop(partner_id, None)

        await bot.send_message(partner_id, "❌ Тень ушла.")
        await message.answer("❌ Тень прекратила общение.")
    else:
        await message.answer("❌ Вы не в чате. Нажмите '🔍 Найти тень'.")

# Stop chat via button
@dp.message(lambda message: message.text == "🛑 Оборвать связь")
async def stop_chat_button(message: types.Message):
    await stop_chat(message)

# Show rules
@dp.message(lambda message: message.text == "📜 Кодекс теней")
async def show_rules(message: types.Message):
    rules_text = (
        "📜 *Кодекс теней:*\n"
        "1️⃣ Проявляй уважение. Собеседник – твое отражение, не оскорбляй его.\n"
        "2️⃣ Запрещены угрозы и тьма. Оскорбления, шантаж, спам – табу.\n"
        "3️⃣ Тени не терпят шума. Флуд и реклама запрещены.\n"
        "4️⃣ Анонимность – наша сила. Не раскрывай личные данные.\n"
        "5️⃣ Нарушение кодекса ведет к изгнанию. Модераторы не прощают ошибок."
    )
    await message.answer(rules_text, parse_mode="Markdown")

# Chat message forwarding
@dp.message()
async def chat_handler(message: types.Message):
    user_id = message.from_user.id

    if user_id in active_chats:
        partner_id = active_chats[user_id]

        if message.text in ["🛑 Оборвать связь", "/stop"]:
            await bot.send_message(partner_id, message.text)
        else:
            delay = random.uniform(1, 3)
            await asyncio.sleep(delay)
            await bot.send_message(partner_id, message.text)
    else:
        await message.answer("❌ Вы не в чате. Нажмите '🔍 Найти тень'.")

# Main function to run the bot
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


with open("README.md", "a", encoding="utf-8") as file:
    file.write("# telegram_bot11\n")

import subprocess

# Define your commit message
commit_message = "Первый коммит"  # Replace with your commit message

# Commit the changes
subprocess.run(["git", "commit", "-m", commit_message])

# Rename the branch to 'main'
subprocess.run(["git", "branch", "-M", "main"])

# Add the remote repository
subprocess.run(["git", "remote", "add", "origin", "https://github.com/Maxhiphop/telegram_bot11.git"])

# Push the changes to the remote repository
subprocess.run(["git", "push", "-u", "origin", "main"])

