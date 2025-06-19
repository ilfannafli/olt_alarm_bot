import telebot
import pymysql
import subprocess
import signal
import os
# inisialisasi Token Bot Kita
bot = telebot.TeleBot('8108321673:AAGMkFTivNWOirWfL3qh2pDVao2tLhohadA')

running = False
permitted_users = [755506334,5940305294] # list User ID dengan izin
tampung_data = {} # Nampung Data

@bot.message_handler(commands=['updatelogin'])
def handle_updatelogin_command(message):
    if message.from_user.id in permitted_users:
        tampung_data[message.from_user.id] = [] # Sesi update baru
        bot.reply_to(message, text="Masukkan username untuk diupdate :")
    else:
        bot.reply_to(message, text="Maaf, tidak berhak melakukan update data login")

@bot.message_handler(func=lambda message: message.from_user.id in tampung_data)
def handle_update_input(message):
    input_baru = message.text
    tampung_data[message.from_user.id].append(input_baru) # masukkan input user ke tampung_data
    if len(tampung_data[message.from_user.id]) == 1:
        bot.reply_to(message, text="Masukkan password baru:")
    elif len(tampung_data[message.from_user.id]) == 2:
        # connect db
        conn = pymysql.connect(host='127.0.0.1',user='root',password='',db='tesoltkp')
        cursor = conn.cursor()
        # memasukkan input ke db
        loginupdate='UPDATE `data_logindummy` SET `pass`="'+tampung_data[message.from_user.id][1]+'" WHERE `user`="'+tampung_data[message.from_user.id][0]+'"'
        cursor.execute(loginupdate)
        conn.commit()
        conn.close()
        #hapus tampung_data
        del tampung_data[message.from_user.id]
        bot.reply_to(message, text="Login data berhasil diupdate.")

@bot.message_handler(commands=['mulaibot'])
def start_program(message):
    if message.from_user.id in permitted_users:
        global running, process
        if not running:
       
            bot.reply_to(message, text="Memulai bot @alarm_mo_mgl_bot")
            try:    
                process = subprocess.Popen(["python", "AIOstart.py"])
                running = True
            except Exception as e:
                bot.send_message(chat_id=message.from_user.id, text="Failed to start the program: {}".format(e))
                return
                
    else:
        bot.reply_to(message, text="Maaf, tidak berhak memulai bot")

@bot.message_handler(commands=['stopbot'])
def start_program(message):
    if message.from_user.id in permitted_users:
        global running, process
        if running:
            kounter=0
            bot.reply_to(message, text="Memberhentikan bot @alarm_mo_mgl_bot")
            while kounter<3:
                with open("pid_thread1.txt", "r") as i:
                    pid = int(i.read().strip())
                    subprocess.call(["taskkill", "/F", "/T", "/PID", str(pid)])
                with open("pid_thread2.txt", "r") as j:
                    pid = int(j.read().strip())
                    subprocess.call(["taskkill", "/F", "/T", "/PID", str(pid)])
                with open("pid_thread3.txt", "r") as k:
                    pid = int(k.read().strip())
                    subprocess.call(["taskkill", "/F", "/T", "/PID", str(pid)])
                with open("pid_battery.txt", "r") as l:
                    pid = int(l.read().strip())
                    subprocess.call(["taskkill", "/F", "/T", "/PID", str(pid)]) 
                with open("pid.txt", "r") as f:
                    pid = int(f.read().strip())
                    subprocess.call(["taskkill", "/F", "/T", "/PID", str(pid)])
                with open("pid_bat.txt", "r") as g:
                    pid = int(g.read().strip())
                    subprocess.call(["taskkill", "/F", "/T", "/PID", str(pid)])
                with open("pid_bot.txt", "r") as h:
                    pid = int(h.read().strip())
                    subprocess.call(["taskkill", "/F", "/T", "/PID", str(pid)])
                kounter+=1
              

            running = False
    else:
        bot.reply_to(message, text="Maaf, tidak berhak memulai bot")

bot.polling()
