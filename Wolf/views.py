

from lib2to3.fixes.fix_input import context


from django.http import HttpResponseRedirect
from django.shortcuts import render , reverse
import sqlite3




def Add_coins_SM(request,amount,User_Id,SM):
    conn = sqlite3.connect('Telegram_bot/db.WolfBotDatabase')
    cursor = conn.cursor()
    cursor.execute("SELECT Instagram_Task, Telegram_Task, YouTube_Task, x_Task FROM users WHERE User_ID = ?", (User_Id,))
    tasks = cursor.fetchall()
    lst_tasks = list(tasks)

    if SM == "Instagram":
        if lst_tasks[0][0] == None:
            try:
                cursor.execute("UPDATE users SET Coin = Coin + ? WHERE User_ID = ?", (amount, User_Id))
                cursor.execute("UPDATE users SET Instagram_Task = TRUE WHERE User_ID = ?", (User_Id,))
                conn.commit()
                if cursor.rowcount > 0:
                    print(f"Coins successfully added to user with ID {User_Id}.")
                else:
                    print(f"No user found with ID {User_Id}.")

            except Exception as e:
                print("An error occurred:", e)
            finally:
                conn.close()
                return HttpResponseRedirect(redirect_to="https://www.instagram.com/thewolf024?igsh=MXZwOHVhZjNjb2d2MA==")
        else:
            return HttpResponseRedirect(redirect_to="https://www.instagram.com/thewolf024?igsh=MXZwOHVhZjNjb2d2MA==")
    elif SM == "Telegram":
        if lst_tasks[0][1] == None:
            try:
                cursor.execute("UPDATE users SET Coin = Coin + ? WHERE User_ID = ?", (amount, User_Id))
                cursor.execute("UPDATE users SET Telegram_Task = TRUE WHERE User_ID = ?", (User_Id,))

                conn.commit()
                if cursor.rowcount > 0:
                    print(f"Coins successfully added to user with ID {User_Id}.")
                else:
                    print(f"No user found with ID {User_Id}.")

            except Exception as e:
                print("An error occurred:", e)
            finally:
                conn.close()
                return HttpResponseRedirect(redirect_to="https://t.me/thewolf057")
        else:
            return HttpResponseRedirect(redirect_to="https://t.me/thewolf057")
    elif SM == "YouTube":
        if lst_tasks[0][2] == None:
            try:
                cursor.execute("UPDATE users SET Coin = Coin + ? WHERE User_ID = ?", (amount, User_Id))
                cursor.execute("UPDATE users SET YouTube_Task = TRUE WHERE User_ID = ?", (User_Id,))

                conn.commit()
                if cursor.rowcount > 0:
                    print(f"Coins successfully added to user with ID {User_Id}.")
                else:
                    print(f"No user found with ID {User_Id}.")

            except Exception as e:
                print("An error occurred:", e)
            finally:
                conn.close()
                return HttpResponseRedirect(redirect_to="https://youtube.com/@thewolf-j1x?si=I9QiOSpWqetxn7vR")
        elif SM == "Daily_gift":
            cursor.execute("UPDATE users SET Coin = Coin + ? WHERE User_ID = ?", (amount, User_Id))


        else:
            return HttpResponseRedirect(redirect_to="https://youtube.com/@thewolf-j1x?si=I9QiOSpWqetxn7vR")
    elif SM == "x":
        if lst_tasks[0][3] == None:
            try:
                cursor.execute("UPDATE users SET Coin = Coin + ? WHERE User_ID = ?", (amount, User_Id))
                cursor.execute("UPDATE users SET x_Task = TRUE WHERE User_ID = ?", (User_Id,))
                conn.commit()
                if cursor.rowcount > 0:
                    print(f"Coins successfully added to user with ID {User_Id}.")
                else:
                    print(f"No user found with ID {User_Id}.")

            except Exception as e:
                print("An error occurred:", e)
            finally:
                return HttpResponseRedirect(redirect_to="https://x.com/thewolf7748?s=09")
        else:
            return HttpResponseRedirect(redirect_to="https://x.com/thewolf7748?s=09")
            conn.close()
    elif SM == "Daily_gift":
        conn = sqlite3.connect('Telegram_bot/db.WolfBotDatabase')
        cursor = conn.cursor()
        cursor.execute("SELECT Daily_gift FROM users WHERE User_ID = ?", (User_Id,))
        s = cursor.fetchone()
        c = s[0]
        Main_Link = reverse("Main_Page", kwargs={"User_Id": User_Id})

        if c == 1 :

            conn = sqlite3.connect("Telegram_bot/db.WolfBotDatabase")
            select = conn.cursor()
            add = conn.cursor()
            select.execute("SELECT Daily_gift FROM users WHERE User_ID = ?", (User_Id,))
            couny = select.fetchall()
            add.execute("UPDATE users SET Coin = Coin + ? WHERE User_ID = ?", (amount, User_Id))
            add.execute("UPDATE users SET Daily_gift = Daily_gift + 1")

            conn.commit()
            return HttpResponseRedirect(redirect_to=Main_Link)
        elif c == 14:
            cursor.execute("UPDATE users SET Daily_gift = 1 WHERE User_ID = ?", (User_Id,) )
            return HttpResponseRedirect(redirect_to=Main_Link)
        else:
            return HttpResponseRedirect(redirect_to=Main_Link)







def Index(request,User_Id):
    conn = sqlite3.connect('Telegram_bot/db.WolfBotDatabase')
    cursor = conn.cursor()
    cursor.execute("SELECT User_ID FROM users ORDER BY Coin DESC")
    rows = cursor.fetchall()
    Userid = [row[0] for row in rows]
    lst_User_Id = []
    for i in Userid:
        if User_Id == i:
            lst_User_Id.append(i)
    conn.close()
    Main_Link = reverse("Main_Page", kwargs={"User_Id": lst_User_Id[0]})
    context = {
        "Main_Link" : Main_Link,
    }
    return render(request,"Wolf/index.html",context)
def Main(request,User_Id):
    inf = []
    conn = sqlite3.connect('Telegram_bot/db.WolfBotDatabase')
    cursor = conn.cursor()
    tasks = conn.cursor()
    tasks.execute("SELECT Instagram_Task, Telegram_Task, YouTube_Task, x_Task FROM users WHERE User_ID = ?", (User_Id,))
    taskses = tasks.fetchall()
    lst_tasks = list(taskses)
    tasks.close()
    lst_info = lst_tasks[0]
    task_info = []
    for task in lst_info:
        if task == None:
            task_info.append("open")
        else:
            task_info.append("done")
    cursor.execute("SELECT * FROM users")
    tables = cursor.fetchall()
    for user in tables:
        if user[1] == int(User_Id):
            inf.append(list(user))
    conn.close()
    data = inf[0]
    Main_Link = reverse("Main_Page",kwargs={"User_Id":User_Id})
    Leaderboard_link = reverse("Leaderboard_Page", kwargs={"User_Id": User_Id})
    Friends_link = reverse("Friends_Page", kwargs={"User_Id": User_Id})
    Crafts_link = reverse("Crafts_Page", kwargs={"User_Id": User_Id})
    Add_coins_SM_Instagram = reverse("Add_coins_SM", kwargs={"amount" : 6000,"User_Id": data[1], "SM" : "Instagram"})
    Add_coins_SM_Telegram = reverse("Add_coins_SM", kwargs={"amount" : 6000,"User_Id": data[1], "SM" : "Telegram"})
    Add_coins_SM_YouTube = reverse("Add_coins_SM", kwargs={"amount" : 6000,"User_Id": data[1], "SM" : "YouTube"})
    Add_coins_SM_x = reverse("Add_coins_SM", kwargs={"amount" : 6000,"User_Id": data[1], "SM" : "x"})
    context = {
        "Id": data[0],
        "User_ID": data[1],
        "User_Name": data[2],
        "First_Name": data[3],
        "Is_Premium": data[4],
        "Coin": data[5],
        "Invites": data[6],
        "Rewards": data[7],
        "Wallet_Address": data[8],
        "len" : data,
        "Main_Link": Main_Link,
        "leaderboard_link" : Leaderboard_link,
        "Friends_link" : Friends_link,
        "Crafts_link" : Crafts_link,
        'Add_coins_SM_Instagram': Add_coins_SM_Instagram,
        "Add_coins_SM_Telegram": Add_coins_SM_Telegram,
        "Add_coins_SM_YouTube" : Add_coins_SM_YouTube,
        "Add_coins_SM_x" : Add_coins_SM_x,
        "task_info" : task_info,


    }
    return render(request, "Wolf/Main Page.html", context)
def Leaderboard(request,User_Id):
    conn = sqlite3.connect('Telegram_bot/db.WolfBotDatabase')
    cursor = conn.cursor()
    cursor.execute("SELECT User_Name, Coin, User_ID FROM users ORDER BY Coin DESC")
    rows = cursor.fetchall()
    num = 1
    users = []
    your_info = []
    coins = []
    for row in rows :
        user = list(row)
        user.append(num)
        users.append(user)
        num += 1
    Your_rang = []

    for user in users:
        coins.append(user[1])
        if user[2] == int(User_Id):
            Your_rang.append(user)

    conn.close()
    Main_Link = reverse("Main_Page", kwargs={"User_Id": Your_rang[0][2]})
    Leaderboard_link = reverse("Leaderboard_Page", kwargs={"User_Id": Your_rang[0][2]})
    Friends_link = reverse("Friends_Page", kwargs={"User_Id": Your_rang[0][2]})
    Crafts_link = reverse("Crafts_Page", kwargs={"User_Id": Your_rang[0][2]})
    context = {
        "Main_Link": Main_Link,
        "leaderboard_link": Leaderboard_link,
        "Friends_link": Friends_link,
        "Crafts_link": Crafts_link,
        "users" : users,
        "Your_info" : your_info,
        "Total_coin" : sum(coins),
        "Your_rang" : Your_rang


    }



    return render(request,"Wolf/Leaderboard Page.html",context)
def Friends(request,User_Id):
    inf = []
    conn = sqlite3.connect('Telegram_bot/db.WolfBotDatabase')  # نام پایگاه داده خود را جایگزین کنید
    cursor = conn.cursor()
    cursor.execute("SELECT User_ID, FL FROM users WHERE User_ID = ?", (User_Id,))
    tables = cursor.fetchall()
    conn.close()
    Main_Link = reverse("Main_Page",kwargs={"User_Id":User_Id})
    Leaderboard_link = reverse("Leaderboard_Page", kwargs={"User_Id": User_Id})
    Friends_link = reverse("Friends_Page", kwargs={"User_Id": User_Id})
    Crafts_link = reverse("Crafts_Page", kwargs={"User_Id": User_Id})
    context = {
        "info" : tables,
        "Main_Link": Main_Link,
        "leaderboard_link": Leaderboard_link,
        "Friends_link": Friends_link,
        "Crafts_link": Crafts_link
    }
    return render(request,"Wolf/Friends Page.html",context)

def daly_gift(request,amount,User_Id):
    conn = sqlite3.connect('Telegram_bot/db.WolfBotDatabase')
    cursor = conn.cursor()
    cursor.execute("SELECT Daily_gift FROM users WHERE User_ID = ?", (User_Id,))
    Daily_gift = cursor.fetchall()



def Crafts(request,User_Id):
    conn = sqlite3.connect('Telegram_bot/db.WolfBotDatabase')
    day = conn.cursor()
    day.execute("SELECT Day FROM users WHERE User_ID = ?", (User_Id,))
    day = day.fetchall()
    day_num = day[0][0]
    Main_Link = reverse("Main_Page",kwargs={"User_Id":User_Id})
    x = 1000
    user_number = int(day_num)
    day_lst = []
    lst = []
    for i in range(user_number):
        day_lst.append(reverse("Add_coins_SM", kwargs={"amount" :x,"User_Id": User_Id,"SM":"Daily_gift" }))
        x += 1000
    while len(day_lst) < 14:
        day_lst.append(Main_Link)
    print(day_lst)




    Main_Link = reverse("Main_Page",kwargs={"User_Id":User_Id})
    Leaderboard_link = reverse("Leaderboard_Page", kwargs={"User_Id": User_Id})
    Friends_link = reverse("Friends_Page", kwargs={"User_Id": User_Id})
    Crafts_link = reverse("Crafts_Page", kwargs={"User_Id": User_Id})
    for i in range(14):
        if i == day_num:
            lst.append("Clime")
            day_num += 1
        else:
            lst.append("Climed")

    context = {
        "day_1" :day_lst[0],
        "day_2" :day_lst[1],
        "day_3" :day_lst[2],
        "day_4" :day_lst[3],
        "day_5" :day_lst[4],
        "day_6" :day_lst[5],
        "day_7" :day_lst[6],
        "day_8" :day_lst[7],
        "day_9" :day_lst[8],
        "day_10" :day_lst[9],
        "day_11" :day_lst[10],
        "day_12" :day_lst[11],
        "day_13" :day_lst[12],
        "day_14" :day_lst[13],
        "day_1_t" : lst[0],
        "day_2_t" : lst[1],
        "day_3_t" : lst[2],
        "day_4_t" : lst[3],
        "day_5_t" : lst[4],
        "day_6_t" : lst[5],
        "day_7_t" : lst[6],
        "day_8_t" : lst[7],
        "day_9_t" : lst[8],
        "day_10_t" : lst[9],
        "day_11_t" : lst[10],
        "day_12_t" : lst[11],
        "day_13_t" : lst[12],
        "day_14_t" : lst[13],
        "Main_Link" : Main_Link,
        "Leaderboard_link" : Leaderboard_link,
        "Friends_link" : Friends_link,
        "Crafts_link" : Crafts_link,

    }
    conn.close()

    return render(request, "Wolf/Crafts Page.html",context)

