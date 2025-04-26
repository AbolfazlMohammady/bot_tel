import threading
from telebot import TeleBot
import sqlite3
import string
import random
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
import time
import schedule
import os
from datetime import datetime

# 🛠 تنظیمات
url = "https://178.156.163.131/"
Token = "7907572327:AAEXa9XsgUvvrKTTxYbv8L5eYtK6gzcp988"
bot = TeleBot(Token)

# 📂 مسیر فایل لاگ
log_file = "log.txt"

# 📝 تابع لاگ نویسی
def write_log(text):
    with open(log_file, "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] {text}\n")

# 📅 تابع اضافه کردن سکه به همه کاربران
def add_coins_to_all_users():
    try:
        conn = sqlite3.connect('db.WolfBotDatabase')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET Coin = Coin + 1000")
        cursor.execute("UPDATE users SET Day = Day + 1")
        cursor.execute("UPDATE users SET Daily_gift = 1")
        conn.commit()
        conn.close()
        write_log("✅ کوین روزانه اضافه شد")
    except Exception as e:
        write_log(f"❌ خطا در اضافه کردن کوین: {e}")

# ⏳ برنامه ریزی فقط یکبار
schedule.every(24).hours.do(add_coins_to_all_users)

# اجرای برنامه زمانبندی در یک ترد جدا
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule, daemon=True).start()

# 📥 هندلر پیام /start
@bot.message_handler(commands=['start'])
def account(message):
    try:
        write_log(f"🚀 /start از {message.from_user.id}")
        conn = sqlite3.connect('db.WolfBotDatabase')
        cursor = conn.cursor()

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

        ckar = string.ascii_letters + string.digits
        link = "".join(random.choice(ckar) for _ in range(20))

        if not existing_user:
            cursor.execute('''
                INSERT INTO users (Id, User_ID, User_Name, First_Name, Is_Premium, Coin, Invites, Rewards, Wallet_Address, FL, Daily_gift, Day)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                1, message.from_user.id, message.from_user.username, message.from_user.first_name,
                message.from_user.is_premium, 0, 0, 0, "", link, 1, 0
            ))
            conn.commit()
            write_log(f"➕ کاربر جدید ثبت شد: {message.from_user.id}")

        # آماده کردن دکمه ها
        web_link_button = InlineKeyboardButton(text="static_Wolf", web_app=WebAppInfo(f"{url}{message.from_user.id}"))
        telegram_link_button = InlineKeyboardButton(text="Join WOLFS Community", url="https://t.me/thewolf057")
        markup = InlineKeyboardMarkup().add(web_link_button, telegram_link_button)

        try:
            photo = open("../Wolf/static/static_Wolf/image/cat.jpg", "rb")
            bot.send_photo(message.chat.id, photo, caption="How cool are you, cat? Let's see it 🐺", reply_markup=markup)
            write_log("📷 عکس ارسال شد.")
        except Exception as e:
            bot.send_message(message.chat.id, "🐺 عکس موجود نیست، اما خوش آمدی!")
            write_log(f"❌ خطا در ارسال عکس: {e}")

        conn.close()

    except Exception as e:
        bot.send_message(message.chat.id, "🚨 خطایی رخ داد، لطفاً دوباره امتحان کن!")
        write_log(f"❌ خطا در اجرای استارت: {e}")

# 🚀 اجرای بی نهایت ربات با مدیریت قطع شدن
while True:
    try:
        write_log("🟢 ربات روشن شد و منتظر پیام هاست...")
        bot.polling(none_stop=True)
    except Exception as e:
        write_log(f"🔴 خطا در ربات: {e}")
        time.sleep(5)  # صبر کنه بعد دوباره تلاش کنه
