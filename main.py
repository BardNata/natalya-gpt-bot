
import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import openai

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Загрузка токенов из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Установка API-ключа OpenAI
openai.api_key = OPENAI_API_KEY

# Приветственное сообщение
WELCOME_MESSAGE = (
    "Готова помочь тебе с Дзеном! Пиши любой вопрос — я подскажу, направлю и помогу. Смелее! Я с тобой 💬"
)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME_MESSAGE)

# Обработчик всех текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    try:
        response = openai.chat.completions.create(
            model="gpt-4",  # Можно заменить на gpt-4 при наличии доступа
            messages=[
                {"role": "system", "content": "Ты — тёплый, человечный помощник по Яндекс Дзене."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content.strip()
        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"Ошибка при обращении к OpenAI: {e}")
        await update.message.reply_text("Ой! Что-то пошло не так. Попробуй ещё раз позже.")

# Запуск приложения
def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
