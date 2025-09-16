import os
import asyncio
from flask import Flask, request
from aiogram import Bot, Dispatcher, types

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def echo(message: types.Message):
    if message.text.lower() == "hi":
        await message.answer("Hello world!")
    elif message.text.lower() == "time":
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await message.answer(f"Current time: {now}")
    else:
        await message.answer("Send 'hi' or 'time'.")

# Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
async def webhook():
    update = types.Update.model_validate(request.get_json())
    await dp.feed_update(bot, update)
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
