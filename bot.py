import random
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters

API_TOKEN = '8059081878:AAFYJBDijfhgBKtW4ictU5NXDH5WFXeRnRY'  # Замените на ваш токен

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Словарь для хранения активных чатов
active_chats = {}

# Команда /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("👋 Привет! Нажми '🔍 Найти тень', чтобы начать.")

# Команда для поиска партнера
@dp.message_handler(filters.Text(equals='🔍 Найти тень'))
async def find_shadow(message: types.Message):
    user_id = message.from_user.id
    
    # Если пользователь уже в чате, уведомляем об этом
    if user_id in active_chats:
        await message.answer("❌ Ты уже в чате. Завершите текущий чат перед началом нового.")
        return

    # Логика поиска партнера (здесь можно добавить свою реализацию)
    for partner_id in active_chats.keys():
        if partner_id != user_id:
            active_chats[user_id] = partner_id
            active_chats[partner_id] = user_id  # Устанавливаем обратное соответствие
            await message.answer("✅ Вы нашли тень!")
            await bot.send_message(partner_id, "✅ Ваш новый собеседник готов к общению!")
            return

    # Если партнер не найден
    active_chats[user_id] = None  # Установим значение None, пока не найдем партнера
    await message.answer("🔍 Ищем тень... Пожалуйста, подождите.")

# Обработка текстовых сообщений
@dp.message_handler(lambda message: message.from_user.id in active_chats)
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    
    if user_id in active_chats:
        partner_id = active_chats[user_id]
        
        if partner_id is not None and partner_id in active_chats:
            try:
                await bot.send_message(partner_id, message.text)
            except Exception as e:
                logging.error(f"Ошибка при отправке сообщения: {e}")
        else:
            await message.answer("❌ Ошибка: ваш чат был потерян. Попробуйте снова найти тень.")
            active_chats.pop(user_id, None)  # Удаляем потерянное соединение
    else:
        await message.answer("❌ Ты не в чате. Нажми '🔍 Найти тень'")

# Запуск бота
async def main():
    await dp.start_polling()

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

