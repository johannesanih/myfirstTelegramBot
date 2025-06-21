from flask import Flask, request
from telebot import TeleBot
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize flask app
app = Flask(__name__)

# Get bot token from environment
TOKEN = os.getenv("BOT_TOKEN")

# Public url
public_url = os.getenv("PUBLIC_URL")

#Webhook url
WEBHOOK_URL = public_url + TOKEN

# Initialize bot
bot = TeleBot(TOKEN)

# Flask route to handle webhook
@app.route("/bot"+TOKEN, methods=["POST"])
def webhook():
    try:
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    except Exception as e:
        return f"Error: {e}", 500

# Command handlers
@bot.message_handler(commands=["start"])
def send_welcome(message):
    try:
        bot.reply_to(message, "Welcome, nice to work for yoy.\nsee /help")
    except Exception as e:
        return f"Error: {e}", 500

@bot.message_handler(commands=['help'])
def send_help(message):
    try:
        bot.reply_to(message, "Available commands:\n/start - Welcome message\n/help - This help message")
    except Exception as e:
        return f"Error: {e}", 500

# Set webhook
def set_webhook():
    try:
        bot.remove_webhook()
        bot.set_webhook(url=WEBHOOK_URL)
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    try:
        set_webhook()
        # Run flask app, 0.0.0.0 for external access
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    except Exception as e:
        print(f"Error: {e}")
