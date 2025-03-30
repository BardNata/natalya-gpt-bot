
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import openai

# Настройка логирования
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Получение токенов из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Ответ по умолчанию
DEFAULT_RESPONSE = "Что-то пошло не так. Попробуй ещё раз или уточни вопрос."

# Обработка входящих сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    logging.info(f"Сообщение от пользователя: {user_message}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты дружелюбный и полезный помощник по Яндекс.Дзену."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.6,
        )
        reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error(f"Ошибка при запросе к OpenAI: {e}")
        reply = DEFAULT_RESPONSE

    await update.message.reply_text(reply)

# Запуск бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Приветственное сообщение при запуске
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "Готова помочь тебе с Дзеном! Пиши любой свой вопрос, и я тебе подскажу ответ или помогу там, где ты в чём-то сомневаешься. Смелее! Я с тобой!"
        )

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.COMMAND, start))

    logging.info("Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
