import paramiko
import time
import requests
import schedule
import pymysql  
from datetime import datetime
import re
from model import train,predict
import telebot

bot = telebot.TeleBot('5955267891:AAHCHgC3K2x4xMMSbDtN6FVrXojkD0EqyDE')
connection = pymysql.connect(host='127.0.0.1',user='root',password='',db='tesoltkp')
cursor = connection.cursor()
#sql_list = 'select ip, versi, hostname, posisi,merk from olt_list;'
sql_list = 'select ip,versi, status from olt_warning;'
cursor.execute(sql_list)
data = cursor.fetchall()

#alamat grup Telegram
url_maingroup = 'https://api.telegram.org/5955267891:AAHCHgC3K2x4xMMSbDtN6FVrXojkD0EqyDE/sendMessage?chat_id=-1001851139717&text='
url_mtcgroup = 'https://api.telegram.org/5955267891:AAHCHgC3K2x4xMMSbDtN6FVrXojkD0EqyDE/sendMessage?chat_id=-1001851139717&text='

#ip, user, password telnet
ip_address = "10.60.190.16"
usr = "940305"
pwd = "Ilfannafli01"
n=0
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=ip_address, username=usr, password=pwd)

print("SSH connection is successfully established with ", ip_address)
start=datetime.time

def func():
    global n
    global cursor
    cursor.execute(sql_list)
    data = cursor.fetchall()
    for olt in data :
    
        n = n+1

        if olt is not None:
            current_load = 1
            bat_percentage = 1
            voltase = 1 
            print(current_load,bat_percentage,voltase)
            shell = ssh.invoke_shell()
            
            #cek ping dulu baru lanjut telnet
            testping = shell.recv(65535)
            shell.send("ping "+olt[0]+" -c 2\n")
            time.sleep(1)
            testping = shell.recv(65535)
            #print(testping.decode())
            print(olt[0])
            shell.send("telnet "+olt[0]+"\n")
            time.sleep(1)
            ceklogin = shell.recv(65535)
            #print(ceklogin.decode())
            shell.send(usr + "\n")
            cekusr = shell.recv(65535)
            #print(cekusr.decode())
            shell.send(pwd + "\n")
            cekpwd = shell.recv(65535)
            #print(cekpwd.decode())
            time.sleep(1)
        
            if olt[1] == "AN5516-04": 
                    cmd = ["cd service",
                            "terminal length 0",
                            "cd .",
                            "cd device",
                            "show hcu env_para card"]

                    for command in cmd:
                        shell.send(command + "\n")
                        time.sleep(0.1)
                        if command == "show hcu env_para card":
                            time.sleep(1)   
                            output = shell.recv(65535)
                            cek = str(output)
                            #print(output.decode())
                            match = re.search(r"total_load_current = (\d+\.\d+)", cek) 
                            match2 = re.search(r"battery_capacity = (\d+\.\d+)", cek)
                            match3 = re.search(r"DC_voltage = (\d+\.\d+)", cek)
                            if match and match2 and match3:
                                bat_percentage = float(match2.group(1))  
                                current_load = str(match.group(1))
                                voltase = str(match3.group(1))

                                print(current_load,bat_percentage,voltase)

                                sisabaterai=bat_percentage*40
                                bat_percentage=str(bat_percentage)
                                sisabaterai=str(sisabaterai)
                                cursor = connection.cursor()
                                sekarang = datetime.now()

                                #cek selisih waktu
                                waktu = sekarang.strftime("%H:%M:%S")
                                lastcheck =  'select time from `test_dropvoltage`;'
                                cursor.execute(lastcheck)
                                firsttime = cursor.fetchone()
                                
                                if firsttime is None :
                                    elapsedsecond=0
                                    elapsedsecond=str(elapsedsecond)
                                    sql_insert_table_warning = 'INSERT INTO `test_dropvoltage`(`ip`,`voltage`,`current_load`,`Percentage`,`capacity`,`time`,`time_elapsed`) VALUES ("'+olt[0]+'","'+voltase+'","'+current_load+'","'+bat_percentage+'","'+sisabaterai+'","'+waktu+'","'+elapsedsecond+'");'
                                    cursor.execute(sql_insert_table_warning)
                                    connection.commit()
                                else :
                                    datetime_object = datetime.strptime(firsttime[0], '%H:%M:%S')
                                    print(datetime_object)
                                    timeelapsed = sekarang - datetime_object
                                    print(timeelapsed)
                                    #timeelapsed = timeelapse.strftime("%H:%M:%S")
                                    #timeelapsed = datetime.strptime(timeelapsed, '%H:%M:%S')
                                  
                                    elapsedsecond = timeelapsed.total_seconds() %86400
                                    elapsedsecond = str(elapsedsecond)
                                    print(timeelapsed)
                                    print(elapsedsecond)
                                    sql_insert_table_warning = 'INSERT INTO `test_dropvoltage`(`ip`,`voltage`,`current_load`,`Percentage`,`capacity`,`time`,`time_elapsed`) VALUES ("'+olt[0]+'","'+voltase+'","'+current_load+'","'+bat_percentage+'","'+sisabaterai+'","'+waktu+'","'+elapsedsecond+'");'
                                    #sql_update_table = 'UPDATE test_dropvoltage SET time_elapsed = UNIX_TIMESTAMP(time) - (SELECT UNIX_TIMESTAMP(MIN(time)) FROM test_dropvoltage);'
                                    cursor.execute(sql_insert_table_warning)
                                    #cursor.execute(sql_update_table)
                                    connection.commit()
                            else :
                                print("Tidak dapat menemukan status baterai untuk OLT ", olt[0] )
                    if n % 15==0 :
                        remaining = predict.predict(olt[0])
                        #train.train(olt[0])
                        remaining = remaining/3600
                        info = "Sisa waktu pada OLT"+olt[0]+"adalah: ",remaining," jam"
                        kirim = str(info)
                        bot.send_message(-1001851139717,kirim)
                        #mess= url_maingroup+str(info)
                        #requests.get(mess)
                        print("Sisa waktu pada OLT"+olt[0]+"adalah: ",remaining," jam")

                        

                #command list untuk OLT versi AN6000-2           
            if olt[1] == "AN6000-2": 
                    cmd = ["config",
                                "terminal length 0",
                                "show hcu card"]
                    for command in cmd:
                        shell.send(command + "\n")
                        time.sleep(0.7)
                        if command == "show hcu card":
                            time.sleep(2)
                            output = shell.recv(65535)
                            #print(output.decode())
                            match = re.search(r"total_load_current = (\d+\.\d+)", str(output))
                            match2 = re.search(r"battery_capacity = (\d+\.\d+)", str(output))
                            match3 = re.search(r"DC_voltage = (\d+\.\d+)", str(output))
                            if match and match2 and match3:
                                bat_percentage = float(match2.group(1))  
                                current_load = str(match.group(1))
                                voltase = str(match3.group(1))

                                print(current_load,bat_percentage,voltase)
                                #hitung sisa baterai
                                sisabaterai=bat_percentage*40
                                bat_percentage=str(bat_percentage)
                                sisabaterai=str(sisabaterai)
                                cursor = connection.cursor()
                                sekarang = datetime.now()
                                print(sekarang)

                                #cek selisih waktu
                                waktu = sekarang.strftime("%H:%M:%S")
                                lastcheck = 'select time from `test_dropvoltage`;'
                                cursor.execute(lastcheck)
                                firsttime = cursor.fetchone()
             
                                if firsttime is None :
                                    elapsedsecond=0
                                    elapsedsecond=str(elapsedsecond)
                                    sql_insert_table_warning = 'INSERT INTO `test_dropvoltage`(`ip`,`voltage`,`current_load`,`Percentage`,`capacity`,`time`,`time_elapsed`) VALUES ("'+olt[0]+'","'+voltase+'","'+current_load+'","'+bat_percentage+'","'+sisabaterai+'","'+waktu+'","'+elapsedsecond+'");'
                                    cursor.execute(sql_insert_table_warning)
                                    connection.commit()
                                else :
                                    datetime_object = datetime.strptime(firsttime[0], '%H:%M:%S')
                                    print(datetime_object)
                                    timeelapsed = sekarang - datetime_object
                                    print(timeelapsed)
                                    #timeelapsed = timeelapse.strftime("%H:%M:%S")
                                    #timeelapsed = datetime.strptime(timeelapsed, '%H:%M:%S')
                                  
                                    elapsedsecond = timeelapsed.total_seconds() %86400
                                    elapsedsecond = str(elapsedsecond)
                                    print(timeelapsed)
                                    print(elapsedsecond)
                                    sql_insert_table_warning = 'INSERT INTO `test_dropvoltage`(`ip`,`voltage`,`current_load`,`Percentage`,`capacity`,`time`,`time_elapsed`) VALUES ("'+olt[0]+'","'+voltase+'","'+current_load+'","'+bat_percentage+'","'+sisabaterai+'","'+waktu+'","'+elapsedsecond+'");'
                                    #sql_update_table = 'UPDATE test_dropvoltage SET time_elapsed = UNIX_TIMESTAMP(time) - (SELECT UNIX_TIMESTAMP(MIN(time)) FROM test_dropvoltage);'
                                    cursor.execute(sql_insert_table_warning)
                                    #cursor.execute(sql_update_table)
                                    connection.commit()
                            else :
                                print("Tidak dapat menemukan status baterai untuk OLT ", olt[0] )
                    
                    if n % 15== 0:
                        remaining = predict.predict(olt[0])
                        #train.train(olt[0])
                        remaining = remaining/3600
                        info = "Sisa waktu pada OLT"+olt[0]+"adalah: ",remaining," jam"
                        kirim = str(info)
                        bot.send_message(-1001851139717,kirim)
                        #mess= url_maingroup+str(info)
                        #requests.get(mess)
                        print("Sisa waktu pada OLT"+olt[0]+"adalah: ",remaining, " jam")
                            

        else:
            print("Tidak ada OLT dalam status warning, menghapus query drop voltage")
            delete_query= 'delete from test_dropvoltage'
            cursor.execute(delete_query)
            connection.commit
            time.sleep(0.2)
            print("Berhasil menghapus query lama")
            continue


schedule.every(3).seconds.do(func)

while True: 
    schedule.run_pending()
#    time.sleep(5)