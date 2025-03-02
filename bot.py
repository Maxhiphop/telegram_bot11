import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

API_TOKEN = ("8059081878:AAFYJBDijfhgBKtW4ictU5NXDH5WFXeRnRY")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Словарь для хранения активных чатов
active_chats = {}
# Очередь пользователей в поиске
search_queue = []

# Клавиатура
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔍 Найти тень")],
        [KeyboardButton(text="📜 Кодекс теней")],
        [KeyboardButton(text="🛑 Оборвать связь")]
    ],
    resize_keyboard=True
)

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Добро пожаловать в общество теней! Нажмите '🔍 Найти тень', чтобы начать поиск собеседника.",
        reply_markup=keyboard
    )

# Поиск собеседника
@dp.message(lambda message: message.text == "🔍 Найти тень")
async def find_chat(message: types.Message):
    user_id = message.from_user.id

    if user_id in active_chats:
        await message.answer("❌ Ты уже говоришь с тенью!")
        return

    if user_id not in search_queue:
        search_queue.append(user_id)

    await message.answer("🔍 Ищем тень... Пожалуйста, подождите.")

    # Если в очереди 2+ человека, соединяем их
    while len(search_queue) >= 2:
        user1 = search_queue.pop(0)
        user2 = search_queue.pop(0)

        active_chats[user1] = user2
        active_chats[user2] = user1

        await bot.send_message(user1, "✅ Тень найдена! Начинайте общение.")
        await bot.send_message(user2, "✅ Тень найдена! Начинайте общение.")

# Оборвать связь
@dp.message(lambda message: message.text == "🛑 Оборвать связь")
async def stop_chat(message: types.Message):
    user_id = message.from_user.id

    if user_id in active_chats:
        partner_id = active_chats.pop(user_id, None)
        if partner_id:
            active_chats.pop(partner_id, None)
            await bot.send_message(partner_id, "❌ Тень ушла. Чат завершен.")
        await message.answer("❌ Ты прервал связь с тенью. Чат завершен.")
    
    elif user_id in search_queue:
        search_queue.remove(user_id)
        await message.answer("❌ Ты отменил поиск собеседника.")
    
    else:
        await message.answer("❌ Ты не в чате. Нажми '🔍 Найти тень'.")

# Кодекс теней
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

# Пересылка сообщений между пользователями
@dp.message(lambda message: True)
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    if user_id in active_chats:
        partner_id =


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

