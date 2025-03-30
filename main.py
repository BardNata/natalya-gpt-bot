import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import openai
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
logging.basicConfig(level=logging.INFO)

# Простой приветственный фильтр
def define_scenario(user_text):
    if "нет" in user_text.lower():
        return "start_from_scratch"
    return "has_channel"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    scenario = define_scenario(user_message)

    if scenario == "has_channel":
        prompt = (
            "Ты — доброжелательный помощник для риелторов, у которых уже есть канал на Дзене. "
            "Ответь в тёплом, дружелюбном тоне и дай совет, как получать больше заявок без рекламы. "
            f"Сообщение от пользователя: {user_message}"
        )
    else:
        prompt = (
            "Ты — доброжелательный помощник для риелторов, у которых ещё нет канала на Дзене. "
            "Объясни спокойно и просто, с чего начать, как придумать название, написать первый пост и не бояться. "
            f"Сообщение от пользователя: {user_message}"
        )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Отвечай тепло, по-человечески, как будто ты Наталья."},
            {"role": "user", "content": prompt}
        ]
    )

    reply_text = response.choices[0].message.content
    await update.message.reply_text(reply_text)

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    app.add_handler(message_handler)
    app.run_polling()