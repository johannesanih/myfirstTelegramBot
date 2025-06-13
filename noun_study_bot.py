import os
from dotenv import load_dotenv
import telebot
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
from datetime import datetime
from scrape import scrape_pdf_links

load_dotenv()


# Use state storage for better control
state_storage = StateMemoryStorage()
BOT_TOKEN = os.getenv("BOT_TOKEN")
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
        InlineKeyboardButton("Science", callback_data="https://nou.edu.ng/ecourseware-faculty-of-sciences/"),
        InlineKeyboardButton("Management Science", callback_data="https://nou.edu.ng/ecourseware-faculty-of-management-sc/"),
        InlineKeyboardButton("Social Science", callback_data="https://nou.edu.ng/ecourseware-faculty-of-social-sc/"),
        InlineKeyboardButton("Health Science", callback_data="https://nou.edu.ng/ecourseware-faculty-of-health-sc/"),
        InlineKeyboardButton("Law", callback_data="https://nou.edu.ng/ecourseware-faculty-of-law/")
        InlineKeyboardButton("Education", callback_data="https://nou.edu.ng/ecourseware-faculty-of-edu/"),
        InlineKeyboardButton("Arts", callback_data="https://nou.edu.ng/ecourseware-faculty-of-arts/")
        InlineKeyboardButton("Agriculture", callback_data="https://nou.edu.ng/ecourseware-faculty-of-agric/"),
        InlineKeyboardButton("DE and General Studies", callback_data="https://nou.edu.ng/ecourseware-degs/"),
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
        bot.reply_to(message, f"Hello! {first_name} Welcome to NOUNStudyBot 📚✨ I'm here to help you find and download course materials for National Open University of Nigeria (NOUN) right here on Telegram. Type /help to get started! 🚀")
    except Exception as e:
        bot.reply_to(message, "Oops, something went wrong! Try again.")
        print(f"Error in start: {e}")

# Help command
@bot.message_handler(commands=['help'])
def send_help(message):
    try:
        bot.reply_to(message, "Available commands:\n/start - Start the Bot\n/help - Show this help message\n/faculty - Get Links to all e-course meatrials from indivaidual faculties")
    except Exception as e:
        bot.reply_to(message, "Oops, something went wrong! Try again.")
        print(f"Error in help: {e}")

# Feedback command with inline keyboard
@bot.message_handler(commands=['faculty'])
def feedback(message):
    try:
        bot.reply_to(message, "What is your faculty of study?", reply_markup=gen_markup())
    except Exception as e:
        bot.reply_to(message, "Oops, something went wrong! Try again.")
        print(f"Error in feedback: {e}")

# Handle inline keyboard callbacks
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        course_pdf_links = []
        if call.data == "https://nou.edu.ng/ecourseware-faculty-of-sciences/":
            course_pdf_links = scrape_pdf_links(call.data)
            bot.answer_callback_query(call.id, "FACULTY OF SCIENCE\n Below are all course materials available in the faculty of science")
            bot.edit_message_text(f"{(",\n").join(course_pdf_links)}", 
                                chat_id=call.message.chat.id, 
                                message_id=call.message.message_id)
        elif call.data == "https://nou.edu.ng/ecourseware-faculty-of-management-sc/":
            course_pdf_links = scrape_pdf_links(call.data)
            bot.answer_callback_query(call.id, "FACULTY OF MANAGEMENT SCIENCE\n Below are all course materials available in the faculty of management science")
            bot.edit_message_text(f"{(",\n").join(course_pdf_links)}", 
                                chat_id=call.message.chat.id, 
                                message_id=call.message.message_id)
        elif call.data == "https://nou.edu.ng/ecourseware-faculty-of-social-sc/":
            course_pdf_links = scrape_pdf_links(call.data)
            bot.answer_callback_query(call.id, "FACULTY OF SOCIAL SCIENCE\n Below are all course materials available in the faculty of social science")
            bot.edit_message_text(f"{(",\n").join(course_pdf_links)}", 
                                chat_id=call.message.chat.id, 
                                message_id=call.message.message_id)
        elif call.data == "https://nou.edu.ng/ecourseware-faculty-of-health-sc/":
            course_pdf_links = scrape_pdf_links(call.data)
            bot.answer_callback_query(call.id, "FACULTY OF HEALTH SCIENCE\n Below are all course materials available in the faculty of health science")
            bot.edit_message_text(f"{(",\n").join(course_pdf_links)}", 
                                chat_id=call.message.chat.id, 
                                message_id=call.message.message_id)
        #
        elif call.data == "https://nou.edu.ng/ecourseware-faculty-of-law/":
            course_pdf_links = scrape_pdf_links(call.data)
            bot.answer_callback_query(call.id, "FACULTY OF LAW\n Below are all course materials available in the faculty of law")
            bot.edit_message_text(f"{(",\n").join(course_pdf_links)}", 
                                chat_id=call.message.chat.id, 
                                message_id=call.message.message_id)
        elif call.data == "https://nou.edu.ng/ecourseware-faculty-of-edu/":
            course_pdf_links = scrape_pdf_links(call.data)
            bot.answer_callback_query(call.id, "FACULTY OF EDUCATION\n Below are all course materials available in the faculty of education")
            bot.edit_message_text(f"{(",\n").join(course_pdf_links)}", 
                                chat_id=call.message.chat.id, 
                                message_id=call.message.message_id)
        elif call.data == "https://nou.edu.ng/ecourseware-faculty-of-arts/":
            course_pdf_links = scrape_pdf_links(call.data)
            bot.answer_callback_query(call.id, "FACULTY OF ARTS\n Below are all course materials available in the faculty of arts")
            bot.edit_message_text(f"{(",\n").join(course_pdf_links)}", 
                                chat_id=call.message.chat.id, 
                                message_id=call.message.message_id)
        elif call.data == "https://nou.edu.ng/ecourseware-faculty-of-agric/":
            course_pdf_links = scrape_pdf_links(call.data)
            bot.answer_callback_query(call.id, "FACULTY OF AGRICULTURE\n Below are all course materials available in the faculty of agriculture")
            bot.edit_message_text(f"{(",\n").join(course_pdf_links)}", 
                                chat_id=call.message.chat.id, 
                                message_id=call.message.message_id)
        elif call.data == "https://nou.edu.ng/ecourseware-degs/":
            course_pdf_links = scrape_pdf_links(call.data)
            bot.answer_callback_query(call.id, "FACULTY OF DE and GENERAL STUDIES\n Below are all course materials available in the faculty of DE and general studies")
            bot.edit_message_text(f"{(",\n").join(course_pdf_links)}", 
                                chat_id=call.message.chat.id, 
                                message_id=call.message.message_id)
            
    except Exception as e:
        bot.answer_callback_query(call.id, "Something went wrong!")
        print(f"Error in callback: {e}")

# Start the bot with error handling
try:
    bot.polling(none_stop=True, interval=0)
except Exception as e:
    print(f"Polling error: {e}")
    bot.reply_to(message, "Bot encountered an error and needs a restart. Please try again later.")