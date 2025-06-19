import pymysql  
import telebot
from model import train,predict
import subprocess

api = '8108321673:AAGMkFTivNWOirWfL3qh2pDVao2tLhohadA'
bot = telebot.TeleBot(api)
running = False
permitted_users = [755506334,5940305294,590479591,91067737] # list User ID dengan izin
tampung_data = {} # Nampung Data
update_olt = {}
edit_olt = {}

@bot.message_handler(commands=['ceklogin'])
def pesan(message):
    connection = pymysql.connect(host='localhost',user='root',password='',db='testoltkp')
    cursor = connection.cursor()

    #AMBIL DATA OLT YANG ACVOLDOWN
    sql_list_acvoldown = 'SELECT `user`, `pass` FROM `data_login`'
    cursor.execute(sql_list_acvoldown)
    data_login = cursor.fetchone()
    info_login ="User = "+data_login[0]+" || Pass = "+data_login[1]
    
    if message.from_user.id in permitted_users:
        bot.reply_to(message, info_login)
    else :
        bot.reply_to(message, text="Tidak diijinkan melihat login")
@bot.message_handler(commands=['cek'])
def pesan(message):
    connection = pymysql.connect(host='localhost',user='root',password='',db='testoltkp')
    cursor = connection.cursor()
    if running :
        #AMBIL DATA OLT YANG ACVOLDOWN
        sql_list_acvoldown = 'SELECT olt_list.hostname, olt_list.ip FROM olt_list join olt_warning on olt_list.ip=olt_warning.ip WHERE olt_warning.status="ACVOLDOWN";'
        cursor.execute(sql_list_acvoldown)
        data_acvoldown = cursor.fetchall()

        sql_list_batmiss = 'SELECT olt_list.hostname, olt_list.ip FROM olt_list join olt_warning on olt_list.ip=olt_warning.ip WHERE olt_warning.status="BATTERY_MISSING";'
        cursor.execute(sql_list_batmiss)
        data_batmiss = cursor.fetchall()

        #AMBIL DATA OLT YANG TERINDIKASI DOWN
        cursor = connection.cursor()
        sql_list_down = 'SELECT olt_list.hostname, olt_list.ip FROM olt_list join olt_down on olt_list.ip=olt_down.ip WHERE olt_down.status="DOWN";'
        cursor.execute(sql_list_down)
        data_down = cursor.fetchall()

        #AMBIL DATA OLT YANG PINTU KABINETNYA TERBUKA
        cursor = connection.cursor()
        sql_list_door = 'SELECT olt_list.hostname, olt_list.ip FROM olt_list join olt_warningdoor on olt_list.ip=olt_warningdoor.ip WHERE olt_warningdoor.status="DOOR_OPEN";'
        cursor.execute(sql_list_door)
        data_door = cursor.fetchall()

        #AMBIL DATA OLT YANG BUNKER BATERAINYA TERBUKA
        cursor = connection.cursor()
        sql_list_bunker = 'SELECT olt_list.hostname, olt_list.ip FROM olt_list join olt_warningdoor on olt_list.ip=olt_warningdoor.ip WHERE olt_warningdoor.status="BUNKER_OPEN";'
        cursor.execute(sql_list_bunker)
        data_bunker = cursor.fetchall()
        
        #Melakukan List pada pintu OLT yang terbuka
        pesan_header_mbt = 'LIST OLT TIDAK TERDAPAT BATERAI:\n '
        pesan_list_mbt = ''
        no_mbt = 0
        for list_mbt in data_batmiss :
            no_mbt += 1        
            pesan_list_mbt = pesan_list_mbt+str(no_mbt)+'. '+list_mbt[0]+' ('+list_mbt[1]+') ' + '\n'
        pesan_mbt = pesan_header_mbt + pesan_list_mbt + '\n'
        
        #Melakukan List pada pintu OLT yang terbuka
        pesan_header_dr = 'LIST OLT PINTU KABINET TERBUKA:\n '
        pesan_list_dr = ''
        no_dr = 0
        for list_dr in data_door :
            no_dr += 1        
            pesan_list_dr = pesan_list_dr+str(no_dr)+'. '+list_dr[0]+' ('+list_dr[1]+') ' + '\n'
        pesan_dr = pesan_header_dr + pesan_list_dr + '\n'


        #Melakukan List pada bunker baterai OLT yang terbuka
        pesan_header_bk = 'LIST OLT BUNKER TERBUKA:\n '
        pesan_list_bk = ''
        no_bk = 0
        for list_bk in data_bunker :
            no_bk += 1        
            pesan_list_bk = pesan_list_bk+str(no_bk)+'. '+list_bk[0]+' ('+list_bk[1]+') ' + '\n'
        pesan_bk = pesan_header_bk + pesan_list_bk + '\n'

        
        #Melakukan List pada OLt yang mati
        pesan_header_av = 'LIST OLT LISTRIK MATI:\n'
        pesan_list_av = ''
        no_av = 0
        for list_av in data_acvoldown :
            cursor=connection.cursor()
            data_bat = 'SELECT voltage, current_load, Percentage FROM test_dropvoltage WHERE ip = %s ORDER BY time DESC LIMIT 1;'
            data_online = 'SELECT online FROM olt_onlineuser WHERE ip = %s ;'
            data_date='select time from `test_dropvoltage` where `ip`=%s ;'
            data_orionline='SELECT online FROM olt_normalonline WHERE ip = %s ;'
            timeelap = 'SELECT time_elapsed FROM test_dropvoltage WHERE ip = %s ORDER BY time DESC LIMIT 1;'
            cursor.execute(data_date,(list_av[1],))
            data_tgl = cursor.fetchone()
            cursor.execute(data_online,(list_av[1],))
            data_on = cursor.fetchone()
            cursor.execute(data_bat,(list_av[1],))
            data_baterai = cursor.fetchone()
            cursor.execute(data_orionline,(list_av[1],))
            data_normon = cursor.fetchone()
            cursor.execute(timeelap,(list_av[1],))
            data_time = cursor.fetchone()
            ektime=data_time[0]
            print(ektime)
            print(type(ektime))
            cektime=float(ektime)
            print(type(cektime))
            print(cektime)
            
            if cektime < 1800:
                print('belum')
                prediksi = "Belum bisa diprediksi"
                jatuhtempo = "-"
            if cektime >=1800:
                #train.train(list_av[1])
                prediksi, jatuhtempo = predict.predict(list_av[1])
                
            no_av += 1        
            print(data_baterai)
            pesan_list_av = pesan_list_av+str(no_av)+'. '+list_av[0]+' ('+list_av[1]+') '+'\n Waktu terdeteksi mati: ('+str(data_tgl[0])+')' + '\n Online User sebelum mati : '+str(data_normon[0])+ '\n ( Voltase = '+str(data_baterai[0])+' | Beban Arus = ' + str(data_baterai[1]) + ' | Sisa Baterai = ' + str(data_baterai[2]) + ' )'+ '\n' +'Online user = '+ str(data_on[0])+'\nPrediksi mati: '+str(prediksi)+' ('+str(jatuhtempo)+') '+'\n'+'\n'
        pesan_av = pesan_header_av + pesan_list_av +'\n'
    
        #Melakukan List pada OLT yang down
        pesan_header_down = 'LIST OLT DOWN:\n'
        pesan_list_down = ''
        no_dw = 0
        for list_down in data_down :
            data_orionline='SELECT online FROM olt_normalonline WHERE ip = %s ;'
            cursor.execute(data_orionline,(list_down[1],))
            data_normon = cursor.fetchone()
            no_dw += 1       
            pesan_list_down = pesan_list_down+str(no_dw)+'. '+list_down[0]+' ('+list_down[1]+') \n Online User sebelum mati : ' +str(data_normon[0])+ '\n\n'
            
        if no_av == 0 and no_dw == 0 and no_bk==0 and no_dr==0: 
                pesan = 'Seluruh OLT UP dan Aman'      
        else:
            pesan_down = pesan_header_down + pesan_list_down + '\n'
            #pesan=pesan_av+pesan_down+pesan_dr+pesan_bk+pesan_mbt
            pesan=pesan_av+pesan_down
        connection.close()    
        bot.reply_to(message, pesan)
    
    if not running:
        bot.reply_to(message, text="Bot belum menyala silahkan gunakan /mulaibot")
    
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
    if message.text.startswith("/"):
        user_input = message.text[1:]
    tampung_data[message.from_user.id].append(input_baru) # masukkan input user ke tampung_data
    
    if len(tampung_data[message.from_user.id]) == 1:
        bot.reply_to(message, text="Masukkan password baru:")
    elif len(tampung_data[message.from_user.id]) == 2:
        # connect db
        conn = pymysql.connect(host='localhost',user='root',password='',db='testoltkp')
        cursor = conn.cursor()
        # memasukkan input ke db
        loginupdate='UPDATE `data_login` SET `pass`="'+tampung_data[message.from_user.id][1]+'" WHERE `user`="'+tampung_data[message.from_user.id][0]+'"'
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
       
            bot.reply_to(message, text="Memulai siklus cek olt")
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
            bot.reply_to(message, text="Memberhentikan siklus olt")
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
        bot.reply_to(message, text="Maaf, tidak berhak memberhentikan siklus cek olt")

@bot.message_handler(commands=['add_olt'])
def handle_add_olt_command(message):
    if message.from_user.id in permitted_users:
        update_olt[message.from_user.id] = []
        bot.reply_to(message, text="Masukkan dengan urutan berikut: \n1.datel\n2.hostname\n3.ip\n4.merk\n5.posisi (OUTDOOR/INDOOR)\n6.sto\n7.versi\n8.thread")
        bot.reply_to(message, text="Masukkan data datel : ")
    else:
        bot.reply_to(message, text="Tidak diizinkan mengupdate database.")

@bot.message_handler(func=lambda message: message.from_user.id in update_olt)
def handle_add_olt_input(message):
    list_data = ['datel','hostname','ip','merk','posisi','sto','versi','thread']
    user_input = message.text
    update_olt[message.from_user.id].append(user_input)
    if len(update_olt[message.from_user.id]) < 8:
        bot.reply_to(message, text=f"Masukkan data {list_data[len(update_olt[message.from_user.id])]}:")
    else:
        conn = pymysql.connect(host='localhost',user='root',password='',db='testoltkp')
        cursor = conn.cursor()
        addolt='INSERT INTO olt_list (datel, hostname, ip, merk, posisi, sto, versi, thread) VALUES ("'+update_olt[message.from_user.id][0]+'", "'+update_olt[message.from_user.id][1]+'", "'+update_olt[message.from_user.id][2]+'", "'+update_olt[message.from_user.id][3]+'", "'+update_olt[message.from_user.id][4]+'", "'+update_olt[message.from_user.id][5]+'", "'+update_olt[message.from_user.id][6]+'", "'+update_olt[message.from_user.id][7]+'")'
        cursor.execute(addolt)
        conn.commit()
        conn.close()
        del update_olt[message.from_user.id]
        bot.reply_to(message, text="Berhasil menambahkan ke database")

@bot.message_handler(commands=['edit_olt'])
def handle_edit_olt_command(message):
    if message.from_user.id in permitted_users:
        edit_olt[message.from_user.id] = []
        bot.reply_to(message, text="Index apa yang akan digunakan untuk mengedit olt ? (hostname/ip)")
    else:
        bot.reply_to(message, text="Tidak diizinkan mengedit database.")

@bot.message_handler(func=lambda message: message.from_user.id in edit_olt)
def handle_edit_olt_input(message):
    user_edit = message.text
    edit_olt[message.from_user.id].append(user_edit)
    if len(edit_olt[message.from_user.id]) < 4:
        if len(edit_olt[message.from_user.id]) == 1:
            bot.reply_to(message, text=f"Pilih "+edit_olt[message.from_user.id][0]+" yang akan diedit :")
        if len(edit_olt[message.from_user.id]) == 2:
            bot.reply_to(message, text=f"Pilih data yang akan diedit (hostname/ip/merk/posisi/sto/versi/thread):")
        if len(edit_olt[message.from_user.id]) == 3:
            bot.reply_to(message, text=f"Masukkan "+edit_olt[message.from_user.id][2]+" baru untuk olt "+edit_olt[message.from_user.id][1]+" : ")

    else:
        conn = pymysql.connect(host='localhost',user='root',password='',db='testoltkp')
        cursor = conn.cursor()
        editolt="UPDATE `olt_list` SET `"+edit_olt[message.from_user.id][2]+"`='"+edit_olt[message.from_user.id][3]+"' WHERE `"+edit_olt[message.from_user.id][0]+"`='"+edit_olt[message.from_user.id][1]+"'"
        bot.reply_to(message, editolt)
        cursor.execute(editolt)
        conn.commit()
        conn.close()
        del edit_olt[message.from_user.id]
        bot.reply_to(message, text="Berhasil mengedit database")

@bot.message_handler(commands=['list'])
def handle_list_command(message):
    bot.reply_to(message, text="List command bot ALMO:\n1./cek = mengecek kondisi berbagai olt\n2./mulaibot = menjalankan siklus cek olt (admin only) \n3./stopbot = menghentikan siklus cek olt (admin only)\n4./ceklogin = mengecek user dan password ssh (admin only)\n5./updatelogin = mengupdate password (admin and dm only)\n6./add_olt = memasukkan olt baru ke database (admin and dm only)\n7./edit_olt = mengedit data olt yang ada di database (admin and dm only)\n8./list = menampilkan list command bot ALMO")
        
while True:
    try:
        bot.polling()
    except:
        pass
