import threading
from telebot import TeleBot
import sqlite3
import string
import random
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
import time
import schedule
import os

url = "http://178.156.163.131/"
Token = "7907572327:AAEXa9XsgUvvrKTTxYbv8L5eYtK6gzcp988"
bot = TeleBot(Token)

@bot.message_handler(commands=['start'])
def account(message):
    if message.text == "/start":
        web_link_button = InlineKeyboardButton(text="static_Wolf", web_app=WebAppInfo(f"{url}{message.from_user.id}"))
        telegram_link_button = InlineKeyboardButton(text="Join WOLFS Community", url="https://t.me/thewolf057")
        markup = InlineKeyboardMarkup().add(web_link_button, telegram_link_button)

        ckar = string.ascii_letters + string.digits
        link = "".join(random.choice(ckar) for _ in range(20))

        # مسیر درست فایل عکس
        current_dir = os.path.dirname(os.path.abspath(__file__))
        photo_path = os.path.join(current_dir, "..", "static", "static_Wolf", "image", "cat.jpg")

        try:
            photo = open(photo_path, "rb")
        except FileNotFoundError:
            photo = None

        text = "How cool are you, cat? Let's see it 🐺 "

        information = {1: {"User_ID": message.from_user.id,
                           "User_Name": message.from_user.username,
                           "First_Name": message.from_user.first_name,
                           "Last_Name": message.from_user.last_name,
                           "Age": "",
                           "Language": message.from_user.language_code,
                           "Is_Premium": message.from_user.is_premium,
                           "Is_bot": message.from_user.is_bot,
                           "Coin" : 0,
                           "Invites" : 0,
                           "Rewards" : 0,
                           "Wallet_Address" : "",
                           "FL" : link,
                           "Daily_gift" : 1,
                           "Day" : 0
                           }}
        user_info = information[1]
        conn = sqlite3.connect('db.WolfBotDatabase')
        cursor = conn.cursor()
    # create table in database and creat value
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        Id INTEGER  ,
        User_ID INTEGER  ,
        User_Name TEXT ,
        First_Name TEXT ,
        Is_Premium BOOLEAN ,
        Coin INTEGER ,
        Invites INTEGER ,
        Rewards INTEGER ,
        Wallet_Address TEXT,
        FL TEXT,
        Instagram_Task BOOLEAN,
        Telegram_Task BOOLEAN,
        YouTube_Task BOOLEAN,
        x_Task BOOLEAN,
        Day INTEGER ,
        Daily_gift INTEGER
    
        )
        ''')
        def add_user(user_id, user_data):
            cursor.execute("SELECT User_Id FROM users")
            user_ids = [row[0] for row in cursor.fetchall()]
            if user_info["User_ID"] not in user_ids:
                cursor.execute('''
                INSERT INTO users (Id, User_ID, User_Name, First_Name,Is_Premium,Coin, Invites, Rewards, Wallet_Address, FL, Daily_gift, Day)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?)
                ''', (user_id, user_data['User_ID'], user_data['User_Name'], user_data['First_Name'], user_data['Is_Premium'],user_data['Coin'], user_data['Invites'], user_data['Rewards'], user_data['Wallet_Address'], user_data['FL'],user_data['Daily_gift'], user_data['Day']))
                conn.commit()
                bot.send_photo(message.chat.id, photo,caption=text,reply_markup=markup)


            else:
                bot.send_photo(message.chat.id, photo,caption=text,reply_markup=markup)
        for user_id, user_data in information.items():
            add_user(user_id, user_data)

        def add_coins_to_all_users():
            # اتصال به پایگاه داده
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

        run_schedule()

        conn.close()

    elif len(message.text.split()) > 1:
        def generate_invite_link(user_id):
            user_links = {}
            conn = sqlite3.connect('db.WolfBotDatabase')
            cursor = conn.cursor()
            cursor.execute("SELECT FL FROM users WHERE User_ID = ?", (user_id,))
            fl_link = list(cursor.fetchall())
            invite_code = list(fl_link)[0][0]
            conn.close()
            user_links[invite_code] = user_id
            print(user_links)
            return f"https://t.me/{bot.get_me().username}?start={invite_code}"
    dict = {}
    conn = sqlite3.connect('db.WolfBotDatabase')
    cursor = conn.cursor()
    cursor.execute("SELECT User_ID, FL FROM users ")
    data = cursor.fetchall()
    list_data = list(data)
    links = dict.values()
    for user in list_data:
        dict[user[0]] = user[1]
    dict_fl = (dict.values())
    if len(message.text.split()) > 1:

        conn = sqlite3.connect('db.WolfBotDatabase')  # نام پایگاه داده خود را جایگزین کنید
        users = conn.cursor()
        users.execute("SELECT User_ID FROM users")
        list_users = list(users.fetchall())
        user_in_data = []
        conn.close()

        for user in list_users:
            user_in_data.append(user[0])
        if message.from_user.id not in user_in_data:
            invite_code = message.text.split()[1]
            invite_id_key = None
            if invite_code in dict_fl:
                for key, value in dict.items():
                    if value == invite_code:
                        invite_id_key = key
                        break
                web_link_button = InlineKeyboardButton(
                text="static_Wolf", 
                web_app=WebAppInfo(f"{url}{message.from_user.id}")
            )
                telegram_link_button = InlineKeyboardButton(
                    text="Join WOLFS Community", 
                    url="https://t.me/thewolf057"
                )
                markup = InlineKeyboardMarkup().add(web_link_button, telegram_link_button)

                ckar = string.ascii_letters + string.digits
                link = "".join(random.choice(ckar) for _ in range(20))

                # ✨ اصلاح مسیر عکس
                current_dir = os.path.dirname(os.path.abspath(__file__))
                photo_path = os.path.join(current_dir, "..", "static", "static_Wolf", "image", "cat.jpg")

                try:
                    photo = open(photo_path, "rb")
                except FileNotFoundError:
                    photo = None

                text = "How cool are you, cat? Let's see it 🐺 "

                information = {1: {"User_ID": message.from_user.id,
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
                                   "Daily_gift" : 1,
                                   "Day" : 0
                                   }}
                user_info = information[1]
                conn = sqlite3.connect('db.WolfBotDatabase')
                cursor = conn.cursor()
                # create table in database and creat value
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                    Id INTEGER  ,
                    User_ID INTEGER  ,
                    User_Name TEXT ,
                    First_Name TEXT ,
                    Is_Premium BOOLEAN ,
                    Coin INTEGER ,
                    Invites INTEGER ,
                    Rewards INTEGER ,
                    Wallet_Address TEXT,
                    FL TEXT,
                    Instagram_Task BOOLEAN,
                    Telegram_Task BOOLEAN,
                    YouTube_Task BOOLEAN,
                    x_Task BOOLEAN,
                    Day INTEGER ,
                    Daily_gift INTEGER


                    )
                    ''')

                def add_user(user_id, user_data):
                    cursor.execute("SELECT User_Id FROM users")
                    user_ids = [row[0] for row in cursor.fetchall()]
                    if user_info["User_ID"] not in user_ids:
                        cursor.execute('''
                            INSERT INTO users (Id, User_ID, User_Name, First_Name,Is_Premium,Coin, Invites, Rewards, Wallet_Address, FL, Daily_gift, Day)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?)
                            ''', (user_id, user_data['User_ID'], user_data['User_Name'], user_data['First_Name'],
                                  user_data['Is_Premium'], user_data['Coin'], user_data['Invites'],
                                  user_data['Rewards'], user_data['Wallet_Address'], user_data['FL'], user_data['Daily_gift'], user_data['Day']))
                        conn.commit()
                        bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)


                    else:
                        bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)

                for user_id, user_data in information.items():
                    add_user(user_id, user_data)
                conn.close()
                conn = sqlite3.connect('db.WolfBotDatabase')  # نام پایگاه داده خود را جایگزین کنید
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET Coin = Coin + ? WHERE User_ID = ?", (10000, invite_id_key))
                cursor.execute("UPDATE users SET Coin = Coin + ? WHERE User_ID = ?", (10000, message.from_user.id))
                conn.commit()

            else:
                bot.send_message(message.chat.id, "لینک دعوت نامعتبر است.")
                bot.send_message(message.chat.id, links)
        else:
            bot.send_message(message.chat.id,text="شما در حال حاضر ار ریات استقاده میکنید")


    else:
        invite_link = generate_invite_link(message.chat.id)
        bot.send_message(message.chat.id, f"سلام {message.from_user.first_name}!\nاین لینک دعوت شماست: {invite_link}")


bot.polling()