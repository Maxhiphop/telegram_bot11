import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

# Токен бота
TOKEN = "8059081878:AAFYJBDijfhgBKtW4ictU5NXDH5WFXeRnRY"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

# Очередь ожидания и активные чаты
waiting_users = []
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

# Логирование
logging.basicConfig(level=logging.INFO)

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Добро пожаловать в элитное общество теней! Нажмите '🔍 Найти тень', чтобы начать.",
        reply_markup=keyboard
    )

# Поиск собеседника (случайный выбор)
@dp.message(lambda message: message.text == "🔍 Найти тень")
async def find_chat(message: types.Message):
    user_id = message.from_user.id
    logging.info(f"Пользователь {user_id} нажал 'Найти тень'.")

    if user_id in active_chats:
        await message.answer("❌ Ты уже говоришь с тенью!")
        return

    if waiting_users:
        partner_id = random.choice(waiting_users)
        waiting_users.remove(partner_id)

        # Устанавливаем чат
        active_chats[user_id] = partner_id
        active_chats[partner_id] = user_id

        # Отправляем уведомления партнерам
        try:
            await bot.send_message(partner_id, "✅ Тень найдена! Начинайте общение.")
            await message.answer("✅ Тень найдена! Начинайте общение.")
            logging.info(f"Чат создан между {user_id} и {partner_id}")
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения партнеру {partner_id}: {e}")
            await message.answer("❌ Произошла ошибка при установке связи. Попробуйте снова.")
    else:
        if user_id not in waiting_users:
            waiting_users.append(user_id)
        await message.answer("⏳ В поисках тени...")

# Остановка чата
async def stop_chat_internal(user_id: int):
    """Закрывает чат между двумя пользователями"""
    if user_id in active_chats:
        partner_id = active_chats.pop(user_id, None)
        if partner_id and partner_id in active_chats:
            active_chats.pop(partner_id, None)
            await bot.send_message(partner_id, "❌ Тень ушла.")
            logging.info(f"Чат между {user_id} и {partner_id} завершен.")
        await bot.send_message(user_id, "❌ Ты прервал связь с тенью.")

# Команда /stop
@dp.message(Command("stop"))
async def stop_chat(message: types.Message):
    user_id = message.from_user.id
    if user_id in active_chats:
        await stop_chat_internal(user_id)
    else:
        await message.answer("❌ Ты не в чате. Нажми '🔍 Найти тень'.")

# Кнопка "Оборвать связь"
@dp.message(lambda message: message.text == "🛑 Оборвать связь")
async def stop_chat_button(message: types.Message):
    await stop_chat(message)

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
@dp.message()
async def chat_handler(message: types.Message):
    user_id = message.from_user.id
    logging.info(f"Обработка сообщения от {user_id}: {message.text}")

    if user_id in active_chats:
        partner_id = active_chats.get(user_id)

        # Проверяем, есть ли партнер в активных чатах
        if partner_id and partner_id in active_chats and active_chats[partner_id] == user_id:
            try:
                await bot.send_message(partner_id, message.text)
                logging.info(f"Сообщение от {user_id} отправлено партнёру {partner_id}")
            except Exception as e:
                logging.error(f"Ошибка при отправке сообщения партнёру {partner_id}: {e}")
                await message.answer("❌ Не удалось отправить сообщение. Попробуйте позже.")
        else:
            await message.answer("❌ Ошибка: ваш чат был потерян. Попробуйте снова найти тень.")
            active_chats.pop(user_id, None)  # Удаляем потерянное соединение
    else:
        logging.info(f"Сообщение от {user_id} не отправлено: не в чате.")
        await message.answer("❌ Вы не в чате. Нажмите '🔍 Найти тень'.")

# Запуск бота
async def main():
    logging.info("Бот запущен.")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при старте бота: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")





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

