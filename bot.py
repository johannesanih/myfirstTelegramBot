import telebot
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
from datetime import datetime

# Use state storage for better control
state_storage = StateMemoryStorage()
BOT_TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (user_id INTEGER PRIMARY KEY, first_name TEXT, last_seen TEXT)''')
    conn.commit()
    conn.close()

# Save or update user data
def save_user(user_id, first_name):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    last_seen = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('''INSERT OR REPLACE INTO users (user_id, first_name, last_seen) 
                 VALUES (?, ?, ?)''', (user_id, first_name, last_seen))
    conn.commit()
    conn.close()

# Create inline keyboard
def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Yes", callback_data="cb_yes"),
        InlineKeyboardButton("No", callback_data="cb_no")
    )
    return markup

# Initialize database
init_db()

# Welcome message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        save_user(user_id, first_name)  # Save user to database
        bot.reply_to(message, "Hello! Welcome to my bot. How can I help you today?")
    except Exception as e:
        bot.reply_to(message, "Oops, something went wrong! Try again.")
        print(f"Error in start: {e}")

# Help command
@bot.message_handler(commands=['help'])
def send_help(message):
    try:
        bot.reply_to(message, "Available commands:\n/start - Welcome message\n/help - Show this help message\n/echo - Echo your message\n/greet - Get a personalized greeting\n/lastseen - Show your last seen time\n/feedback - Give feedback with buttons")
    except Exception as e:
        bot.reply_to(message, "Oops, something went wrong! Try again.")
        print(f"Error in help: {e}")

# Echo command
@bot.message_handler(commands=['echo'])
def echo_message(message):
    try:
        text = message.text[6:].strip()
        if text:
            bot.reply_to(message, f"You said: {text}")
        else:
            bot.reply_to(message, "Please provide a message to echo! Example: /echo Hello")
    except Exception as e:
        bot.reply_to(message, "Oops, something went wrong! Try again.")
        print(f"Error in echo: {e}")

# Personalized greeting
@bot.message_handler(commands=['greet'])
def greet_user(message):
    try:
        user_name = message.from_user.first_name
        bot.reply_to(message, f"Nice to meet you, {user_name}! How’s your day going?")
    except Exception as e:
        bot.reply_to(message, "Oops, something went wrong! Try again.")
        print(f"Error in greet: {e}")

# Last seen command
@bot.message_handler(commands=['lastseen'])
def last_seen(message):
    try:
        user_id = message.from_user.id
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute("SELECT last_seen FROM users WHERE user_id = ?", (user_id,))
        result = c.fetchone()
        conn.close()
        if result:
            bot.reply_to(message, f"You were last seen on: {result[0]}")
        else:
            bot.reply_to(message, "No record found. Try interacting with me first!")
    except Exception as e:
        bot.reply_to(message, "Oops, something went wrong! Try again.")
        print(f"Error in lastseen: {e}")

# Feedback command with inline keyboard
@bot.message_handler(commands=['feedback'])
def feedback(message):
    try:
        bot.reply_to(message, "Do you like this bot?", reply_markup=gen_markup())
    except Exception as e:
        bot.reply_to(message, "Oops, something went wrong! Try again.")
        print(f"Error in feedback: {e}")

# Handle inline keyboard callbacks
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == "cb_yes":
            bot.answer_callback_query(call.id, "Glad you like it!")
            bot.edit_message_text("Thanks for the positive feedback!", 
                                chat_id=call.message.chat.id, 
                                message_id=call.message.message_id)
        elif call.data == "cb_no":
            bot.answer_callback_query(call.id, "Sorry to hear that!")
            bot.edit_message_text("Thanks for the feedback. We'll improve!", 
                                chat_id=call.message.chat.id, 
                                message_id=call.message.message_id)
    except Exception as e:
        bot.answer_callback_query(call.id, "Something went wrong!")
        print(f"Error in callback: {e}")

# Handle photos
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        bot.reply_to(message, "Wow, nice photo! I’ve received it.")
    except Exception as e:
        bot.reply_to(message, "Oops, something went wrong! Try again.")
        print(f"Error in photo: {e}")

# Handle stickers
@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    try:
        sticker_id = message.sticker.file_id
        bot.reply_to(message, "Cool sticker! Sending it back!")
        bot.send_sticker(message.chat.id, sticker_id)
    except Exception as e:
        bot.reply_to(message, "Oops, something went wrong with the sticker!")
        print(f"Error in sticker: {e}")

# Handle text messages
@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        save_user(user_id, first_name)  # Update last seen
        bot.reply_to(message, "I got your message! Try /help for commands.")
    except Exception as e:
        bot.reply_to(message, "Oops, something went wrong! Try again.")
        print(f"Error in text: {e}")

# Start the bot with error handling
try:
    bot.polling(none_stop=True, interval=0)
except Exception as e:
    print(f"Polling error: {e}")
    bot.reply_to(message, "Bot encountered an error and needs a restart. Please try again later.")