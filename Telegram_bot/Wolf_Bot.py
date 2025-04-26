import threading
from telebot import TeleBot
import sqlite3
import string
import random
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
import time
import schedule

# 🛠 تنظیمات
url = "https://178.156.163.131/"  # آدرس سرور
Token = "7907572327:AAEXa9XsgUvvrKTTxYbv8L5eYtK6gzcp988"  # توکن ربات
bot = TeleBot(Token)

# 📅 تابع اضافه کردن سکه به همه‌ی کاربران هر ۲۴ ساعت
def add_coins_to_all_users():
    conn = sqlite3.connect('db.WolfBotDatabase')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET Coin = Coin + 1000")
    cursor.execute("UPDATE users SET Day = Day + 1")
    cursor.execute("UPDATE users SET Daily_gift = 1")
    conn.commit()
    conn.close()

# ⏳ اجرای زمان‌بندی به صورت ترد جداگانه
schedule.every(24).hours.do(add_coins_to_all_users)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule, daemon=True).start()

# 📥 هندل کردن پیام start
@bot.message_handler(commands=['start'])
def account(message):
    conn = sqlite3.connect('db.WolfBotDatabase')
    cursor = conn.cursor()

    # ساخت دکمه‌ی وب و گروه
    web_link_button = InlineKeyboardButton(text="static_Wolf", web_app=WebAppInfo(f"{url}{message.from_user.id}"))
    telegram_link_button = InlineKeyboardButton(text="Join WOLFS Community", url="https://t.me/thewolf057")
    markup = InlineKeyboardMarkup().add(web_link_button, telegram_link_button)

    # ساخت یک لینک تصادفی برای فل (FL)
    ckar = string.ascii_letters + string.digits
    link = "".join(random.choice(ckar) for _ in range(20))

    # اطلاعات کاربر
    information = {
        1: {
            "User_ID": message.from_user.id,
            "User_Name": message.from_user.username,
            "First_Name": message.from_user.first_name,
            "Last_Name": message.from_user.last_name,
            "Age": "",
            "Language": message.from_user.language_code,
            "Is_Premium": message.from_user.is_premium,
            "Is_bot": message.from_user.is_bot,
            "Coin": 0,
            "Invites": 0,
            "Rewards": 0,
            "Wallet_Address": "",
            "FL": link,
            "Daily_gift": 1,
            "Day": 0
        }
    }
    user_info = information[1]

    # ساخت جدول کاربران در دیتابیس
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

    # تابع اضافه کردن کاربر
    def add_user(user_id, user_data):
        cursor.execute("SELECT User_ID FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]
        if user_data["User_ID"] not in user_ids:
            cursor.execute('''
                INSERT INTO users (Id, User_ID, User_Name, First_Name, Is_Premium, Coin, Invites, Rewards, Wallet_Address, FL, Daily_gift, Day)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, user_data['User_ID'], user_data['User_Name'], user_data['First_Name'],
                user_data['Is_Premium'], user_data['Coin'], user_data['Invites'],
                user_data['Rewards'], user_data['Wallet_Address'], user_data['FL'],
                user_data['Daily_gift'], user_data['Day']
            ))
            conn.commit()
        
        # فرستادن عکس خوش آمدگویی
        photo = open("../Wolf/static/static_Wolf/image/cat.jpg", "rb")
        text = "How cool are you, cat? Let's see it 🐺 "
        bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)

    for user_id, user_data in information.items():
        add_user(user_id, user_data)

    conn.close()

# ✅ بعد از تمام تعریف‌ها، ربات شروع به گوش دادن پیام‌ها می‌کند
bot.polling()
