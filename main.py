import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import openai
import os

openai.api_key = os.getenv("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")
TELEGRAM_TOKEN = os.getenv("7392121079:AAGeWxyeFROtTE0kDm7FlkiqO6UYBwLu9UU")

SYSTEM_MESSAGE = (
    "Ты — помощник Натальи, специалиста по новостройкам Москвы. "
    "Общаешься с риелторами — тепло, по-человечески, без официоза. "
    "Поддерживаешь, вдохновляешь, помогаешь. Не используй кнопки. Только текст. "
    "Если человек новичок — подскажи, с чего начать. Если опытный — помоги усилить контент."
)

async def ask_chatgpt(message):
    client = openai.OpenAI()
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Произошла ошибка при обращении к ChatGPT: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот-помощник Натальи. Готова помочь с Дзеном 😊")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = await ask_chatgpt(user_message)
    await update.message.reply_text(reply)

async def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
