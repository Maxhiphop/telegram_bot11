import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

API_TOKEN = "8059081878:AAFYJBDijfhgBKtW4ictU5NXDH5WFXeRnRY"  # Вставь свой токен

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Словарь для хранения активных чатов
active_chats = {}

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
        "Добро пожаловать в элитное общество теней! Нажмите '🔍 Найти тень', чтобы начать.",
        reply_markup=keyboard
    )

# Поиск собеседника
@dp.message(F.text == "🔍 Найти тень")
async def find_chat(message: types.Message):
    user_id = message.from_user.id

    if user_id in active_chats and active_chats[user_id] is not None:
        await message.answer("❌ Ты уже говоришь с тенью!")
        return

    # Ищем свободного собеседника
    for partner_id in active_chats.keys():
        if active_chats[partner_id] is None:
            active_chats[user_id] = partner_id
            active_chats[partner_id] = user_id
            await message.answer("✅ Тень найдена! Начинайте общение.")
            await bot.send_message(partner_id, "✅ Тень найдена! Начинайте общение.")
            return

    # Если нет свободных, ставим в очередь
    active_chats[user_id] = None
    await message.answer("🔍 Ищем тень... Пожалуйста, подождите.")

# Оборвать связь
@dp.message(F.text == "🛑 Оборвать связь")
async def stop_chat(message: types.Message):
    user_id = message.from_user.id

    if user_id in active_chats:
        partner_id = active_chats.pop(user_id, None)
        if partner_id and partner_id in active_chats:
            active_chats.pop(partner_id, None)
            await bot.send_message(partner_id, "❌ Тень ушла. Чат завершен.")
        await message.answer("❌ Ты прервал связь с тенью. Чат завершен.")
    else:
        await message.answer("❌ Ты не в чате. Нажми '🔍 Найти тень'.")

# Кодекс теней
@dp.message(F.text == "📜 Кодекс теней")
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
@dp.message(F.text)
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    if user_id in active_chats and active_chats[user_id] is not None:
        partner_id = active_chats[user_id]

        if partner_id in active_chats and active_chats[partner_id] == user_id:
            try:
                await bot.send_message(partner_id, message.text)
            except Exception as e:
                logging.error(f"Ошибка при отправке сообщения: {e}")
        else:
            await message.answer("🔍 Ты в поиске, подожди собеседника.")
    else:
        await message.answer("❌ Ты не в чате. Нажми '🔍 Найти тень'.")

# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
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

