from flask import Flask, request
from telebot import Telebot
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize flask app
app = Flask(__name__)

# Get bot token from environment
TOKEN = os.getenv("BOT_TOKEN")

# Public url
public_url = ""

#Webhook url
WEBHOOK_URL = public_url + TOKEN

# Initialize bot
bot = Telebot(TOKEN)

# Flask route to handle webhook
@app.route("/"+TOKEN, methods=["POST"])
def webhook():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

# Command handlers
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Welcome, nice to work for yoy.\nsee /help")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Available commands:\n/start - Welcome message\n/help - This help message")

# Set webhook
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(URL=WEBHOOK_URL)

if __name__ == "__main__":
    set_webhook()
    # Run flask app, 0.0.0.0 for external access
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
