import threading
from telebot import TeleBot
import sqlite3
import string
import random
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
import time
import schedule

url = "https://178.156.163.131/"
Token = "7907572327:AAEXa9XsgUvvrKTTxYbv8L5eYtK6gzcp988"
bot = TeleBot(Token)

def add_coins_to_all_users():
    conn = sqlite3.connect('db.WolfBotDatabase')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET Coin = Coin + 1000")
    cursor.execute("UPDATE users SET Day = Day + 1")
    cursor.execute("UPDATE users SET Daily_gift = 1")
    conn.commit()
    conn.close()

schedule.every(24).hours.do(add_coins_to_all_users)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule, daemon=True).start()

@bot.message_handler(commands=['start'])
def account(message):
    print("/start دریافت شد")  # فقط برای تست کنسول

    # بعدش اطلاعات دیتابیس و دکمه‌ها و بقیه رو اجرا کن
    conn = sqlite3.connect('db.WolfBotDatabase')
    cursor = conn.cursor()

    web_link_button = InlineKeyboardButton(text="static_Wolf", web_app=WebAppInfo(f"{url}{message.from_user.id}"))
    telegram_link_button = InlineKeyboardButton(text="Join WOLFS Community", url="https://t.me/thewolf057")
    markup = InlineKeyboardMarkup().add(web_link_button, telegram_link_button)

    photo = open("../Wolf/static/static_Wolf/image/cat.jpg", "rb")
    text = "How cool are you, cat? Let's see it 🐺 "

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            Id INTEGER,
            User_ID INTEGER,
            User_Name TEXT,
            First_Name TEXT,
            Is_Premium BOOLEAN,
            Coin INTEGER,
            Invites INTEGER,
            Rewards INTEGER,
            Wallet_Address TEXT,
            FL TEXT,
            Instagram_Task BOOLEAN,
            Telegram_Task BOOLEAN,
            YouTube_Task BOOLEAN,
            x_Task BOOLEAN,
            Day INTEGER,
            Daily_gift INTEGER
        )
    ''')

    cursor.execute("SELECT User_ID FROM users WHERE User_ID = ?", (message.from_user.id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        cursor.execute('''
            INSERT INTO users (Id, User_ID, User_Name, First_Name, Is_Premium, Coin, Invites, Rewards, Wallet_Address, FL, Daily_gift, Day)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            1, message.from_user.id, message.from_user.username, message.from_user.first_name,
            message.from_user.is_premium, 0, 0, 0, "", "", 1, 0
        ))
        conn.commit()

    bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)
    conn.close()

# 👇👇👇 آخر آخر فایل
print("ربات روشن شد و آماده دریافت پیام هاست...")
bot.polling()
