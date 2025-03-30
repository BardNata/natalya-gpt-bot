
import logging
import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Получение токенов из переменных среды
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Настройка OpenAI
openai.api_key = OPENAI_API_KEY

# Приветственное сообщение
WELCOME_MESSAGE = (
    "Готова помочь тебе с Дзеном! Пиши любой свой вопрос, и я тебе подскажу ответ "
    "или помогу там, где ты в чём-то сомневаешься. Смелее! Я с тобой!"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты — помощник по Яндекс.Дзен, отвечаешь понятно и дружелюбно."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Ошибка OpenAI: {e}")
        reply = "Что-то пошло не так. Попробуй ещё раз."

    await update.message.reply_text(reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
