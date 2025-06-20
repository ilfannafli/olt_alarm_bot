import paramiko
import time
import requests
import schedule
import pymysql  
from datetime import datetime
import re
from model import train,predict
import telebot
import math as mt
from getfunc import getLoginData, getGroupID
from checkfunc import sendCommand
import os
pid = os.getpid()
with open("pid_battery.txt", "w") as file:
    file.write(str(pid)) 


bot = telebot.TeleBot('8108321673:AAGMkFTivNWOirWfL3qh2pDVao2tLhohadA')
#connection = pymysql.connect(host='localhost',user='root',password='',db='tesoltkp')
#cursor = connection.cursor()
#sql_list = 'select ip, versi, hostname, posisi,merk from olt_list;'
#sql_list = 'select ip,versi, status from olt_warning;'
#cursor.execute(sql_list)
#data = cursor.fetchall()
connection = pymysql.connect(host='localhost',user='root',password='',db='testoltkp')
url_maingroup,url_mtcgroup,url_kpgroup, url_patroligroup, ip_address,usr,pwd = getLoginData.custom(connection)
#alamat grup Telegram
#url_maingroup = 'https://api.telegram.org/5955267891:AAHCHgC3K2x4xMMSbDtN6FVrXojkD0EqyDE/sendMessage?chat_id=-1001851139717&text='
#url_mtcgroup = 'https://api.telegram.org/5955267891:AAHCHgC3K2x4xMMSbDtN6FVrXojkD0EqyDE/sendMessage?chat_id=-1001851139717&text='
#url_maingroup = 'https://api.telegram.org/bot5955267891:AAHCHgC3K2x4xMMSbDtN6FVrXojkD0EqyDE/sendMessage?chat_id=-1001851139717&text='
#url_mtcgroup = 'https://api.telegram.org/bot5933357528:AAGoECge8eGvPFQqG3Y1xfXeA3-yu-tVy8Q/sendMessage?chat_id=-865403076&text='
#ip, user, password telnet
#ip_address = "10.60.190.16"
#usr = "940305"
#pwd = "Ilfannafli01"
n=[0,0,0,0,0,0,0,0,0]
floorsec=[0,0,0,0,0,0,0,0,0]
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=ip_address, username=usr, password=pwd)

#print("SSH connection is successfully established with ", ip_address)
start=datetime.time
    
 
def func():
    global n
    global floorsec
    i=0
    #ip, user, password telnet
    #ip_address = "10.60.190.16"
    #usr = "940305"
    #pwd = "Ilfannafli01"
    #ssh = paramiko.SSHClient()
    #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect(hostname=ip_address, username=usr, password=pwd)
   # print("SSH connection is successfully established with ", ip_address)

    #print("SSH connection is successfully established with ", ip_address)
    #global cursor
    connection = pymysql.connect(host='localhost',user='root',password='',db='testoltkp')
    cursor = connection.cursor()
    data=()
    #print(len(data))
    sql_list = 'select ip,versi, status, hostname from olt_warning where status="ACVOLDOWN";'
    cursor.execute(sql_list)
    data = cursor.fetchall()
    
    data_dropvoltage=()
    drop_voltage = 'select ip,voltage,current_load,Percentage,capacity,time,time_elapsed from test_dropvoltage;'
    cursor.execute(drop_voltage)
    data_dropvoltage=cursor.fetchall()
    #print(len(data))
    #print(len(data_dropvoltage))


    if len(data) == 0: 
        if len(data_dropvoltage) != 0:
            print("Tidak ada OLT dalam status warning, menghapus query drop voltage\n")
            delete_query= 'DELETE FROM test_dropvoltage'
            delete_onlineuser='DELETE FROM olt_onlineuser'
            cursor.execute(delete_query)
            connection.commit()
            cursor.execute(delete_onlineuser)
            connection.commit()
            print("Berhasil menghapus tabel lama")
            
        time.sleep(0.2)
        n=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        floorsec=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        

    else : 
        for olt in data :
            current_load = 1
            bat_percentage = 1
            voltase = 1 
            voltaseAC = 1
            #print(current_load,bat_percentage,voltase)
            #shell = ssh.invoke_shell()
            #cek ping dulu baru lanjut telnet
            #testping = shell.recv(65535)
            #shell.send("ping "+olt[0]+" -c 2\n")
            #print(testping.decode())
            shell = ssh.invoke_shell()
            print(olt[3])
            sendCommand.wait_for_output(shell, olt[3], "telnet "+olt[0]+"\n", "Login")
            sendCommand.wait_for_output(shell, olt[3], usr + "\n", "Password")
            sendCommand.wait_for_output(shell, olt[3], pwd + "\n", "#") 
            if olt[1] == "AN5516-04" and olt[2] =="ACVOLDOWN": 
                  
                i=i+1
                #print("--> ", n[i])
                #n[i] = n[i]+1
                #print("-----> ",n[i])
                sendCommand.wait_for_output(shell, olt[3], "cd service\n", "#")
                sendCommand.wait_for_output(shell, olt[3], "terminal length 0\n", "#")
                sendCommand.wait_for_output(shell, olt[3], "cd .\n", "#")
                sendCommand.wait_for_output(shell, olt[3], "cd device\n", "#")
                output = sendCommand.wait_for_output(shell, olt[3], "show hcu env_para card\n", "#")
                
                cek = str(output)
                print(output)
                match = re.search(r"total_load_current = (\d+\.\d+)", cek) 
                match2 = re.search(r"battery_capacity = (\d+\.\d+)", cek)
                match3 = re.search(r"DC_voltage = (\d+\.\d+)", cek)
                match4 = re.search(r"AC_voltage_R = (\d+\.\d+)", str(output))
                
                if match and match2 and match3:
                    bat_percentage = float(match2.group(1))  
                    current_load = str(match.group(1))
                    voltase = str(match3.group(1))
                    voltaseAC = str(match4.group(1))

                    print(current_load,bat_percentage,voltase)

                    sisabaterai=bat_percentage*40
                    bat_percentage=str(bat_percentage)
                    sisabaterai=str(sisabaterai)
                    cursor = connection.cursor()
                    sekarang = datetime.now()

                    #cek selisih waktu
                    waktu = sekarang.strftime("%Y-%m-%d %H:%M:%S")
                    lastcheck =  'select time from `test_dropvoltage` where `ip`="'+olt[0]+'";'
                    cursor.execute(lastcheck)
                    firsttime = cursor.fetchone()      
                    
                    #cek online user
                    sendCommand.wait_for_output(shell, olt[3], "cd /\n", "#")
                    sendCommand.wait_for_output(shell, olt[3], "cd onu\n", "#")
                    outputonline = sendCommand.wait_for_output(shell, olt[3], "show onu auth-and-online statistics level system\n", "#")
                    onlinecheck =  'select online from `olt_onlineuser` where `ip`="'+olt[0]+'";'
                    cursor.execute(onlinecheck)
                    onlinecheck = cursor.fetchone()
                    #outputonline =shell.recv(65535)
                    print(outputonline)
                    outputonline=str(outputonline)
                    onlinematch = re.search(r"\d+/\d+ ", outputonline)  
                    if onlinematch:
                        if onlinecheck is None :
                            useronline = onlinematch.group(0)
                            useronline = str(useronline)
                            tableonline= 'INSERT INTO `olt_onlineuser`(`ip`, `hostname`, `online`) VALUES ("'+olt[0]+'","'+olt[3]+'","'+useronline+'");'
                            cursor.execute(tableonline)
                            connection.commit()   
                        useronline = onlinematch.group(0)
                        useronline = str(useronline)
                        tableonline= 'UPDATE `olt_onlineuser` SET `online`="'+useronline+'" WHERE `ip`="'+olt[0]+'";'
                        cursor.execute(tableonline)
                        connection.commit()
                        
                    #cek apakah data baru dimasukkan pertama kali    
                    if firsttime is None:
                        #cek lagi sudah hilang apa belum
                        doublecheck = 'select hostname from olt_warning where `ip`  ="'+olt[0]+'";'
                        cursor.execute(doublecheck)
                        checkWarning = cursor.fetchone()

                        if checkWarning is not None:
                            elapsedsecond=0
                            elapsedsecond=str(elapsedsecond)
                            sql_insert_table_warning = 'INSERT INTO `test_dropvoltage`(`ip`,`voltage`,`current_load`,`Percentage`,`capacity`,`time`,`time_elapsed`) VALUES ("'+olt[0]+'","'+voltase+'","'+current_load+'","'+bat_percentage+'","'+sisabaterai+'","'+waktu+'","'+elapsedsecond+'");'
                            cursor.execute(sql_insert_table_warning)
                            connection.commit()
                            if float(voltaseAC) > 0:
                                firstingfo="listrik "+olt[3]+" tidak mati, voltase AC saat ini down, sebesar: "+ voltaseAC+" V"
                            else:
                                firstingfo="STATUS "+olt[3]+" : VOLTASE DC = " + voltase + " | VOLTASE AC = " + voltaseAC + " | ARUS BEBAN = " +current_load+" | ONLINE USER = "+useronline
                            
                            #bot.send_message(-1001851139717,firstingfo)
                            msg_maingroup = url_maingroup+firstingfo
                            requests.get(msg_maingroup)

                            #cek id grup
                            grupWitel = getGroupID.getID(connection,olt[0])
                            msg_grupWitel = grupWitel + firstingfo
                            requests.get(msg_grupWitel,timeout=5)
                            
                            '''msg_mtcgroup = url_mtcgroup+firstingfo
                            requests.get(msg_mtcgroup)'''
                            n[i]=0
                            floorsec[i] = 0
                    else :
                        #cek lagi sudah hilang apa belum
                        doublecheck = 'select hostname from olt_warning where `ip`="'+olt[0]+'";'
                        cursor.execute(doublecheck)
                        checkWarning = cursor.fetchone()
                        if checkWarning is not None:
                            #print(firsttime[0])
                            datetime_object = datetime.strptime(firsttime[0], '%Y-%m-%d %H:%M:%S')
                            #print(datetime_object)
                            timeelapsed = sekarang - datetime_object
                            #print(timeelapsed)
                            #timeelapsed = timeelapsed.strftime("%H:%M:%S")
                            #timeelapsed = datetime.strptime(timeelapsed, '%H:%M:%S')
                            
                            elapsedsecond = timeelapsed.total_seconds() #%86400
                            floorsec[i] = mt.floor(elapsedsecond/1800)
                            #print("FLOORSEC-----> ",floorsec[i])
                            #n[i]=floorsec
                            elapsedsecond = str(elapsedsecond)
                            #print(timeelapsed)
                            #print(elapsedsecond)

                            

                            sql_insert_table_warning = 'INSERT INTO `test_dropvoltage`(`ip`,`voltage`,`current_load`,`Percentage`,`capacity`,`time`,`time_elapsed`) VALUES ("'+olt[0]+'","'+voltase+'","'+current_load+'","'+bat_percentage+'","'+sisabaterai+'","'+waktu+'","'+elapsedsecond+'");'
                            #sql_update_table = 'UPDATE test_dropvoltage SET time_elapsed = UNIX_TIMESTAMP(time) - (SELECT UNIX_TIMESTAMP(MIN(time)) FROM test_dropvoltage);'
                            cursor.execute(sql_insert_table_warning)
                            #cursor.execute(sql_update_table)
                            connection.commit()
                            #print("-----> ",n[i])
                else :
                    print("Tidak dapat menemukan status baterai untuk OLT ", olt[0] )
                
                #Cek untuk melakukan training dan prediksi
                if floorsec[i] != n[i] and floorsec[i] !=0 :
                    # print("PREDICT TIME KE - ", floorsec[i])
                    n[i]=floorsec[i]
                    train.train(olt[0])
                    remaining, jatuhtempo = predict.predict(olt[0])
                    #remaining = remaining/3600
                    #remaining = str(remaining)
                    info = "Sisa waktu pada OLT "+olt[3]+" ("+olt[0]+") adalah: "+remaining+" dengan predikisi mati pada : "+jatuhtempo+" ( Voltase DC = "+voltase+" | Voltase AC = "+voltaseAC+" | Sisa baterai = "+bat_percentage+" | Beban Arus = " +current_load+" | Online User = "+useronline+" )"
                    #kirim = str(info)
                    #bot.send_message(-1001851139717,info)
                    msg_maingroup = url_maingroup+info
                    requests.get(msg_maingroup)

                    #cek id grup
                    grupWitel = getGroupID.getID(connection,olt[0])
                    msg_grupWitel = grupWitel + info
                    requests.get(msg_grupWitel)
                    '''msg_mtcgroup = url_mtcgroup+info
                    requests.get(msg_mtcgroup)    '''                   
                    #mess= url_maingroup+str(info)
                    #requests.get(mess)
                    #print("Sisa waktu pada OLT "+olt[3]+" ("+olt[0]+") adalah: "+remaining+" jam ,( Voltase = "+voltase+" | Sisa baterai = "+bat_percentage+" | Beban Arus = " +current_load )

                        

                #command list untuk OLT versi AN6000-2           
            if olt[1] == "AN6000-2" and olt[2] == "ACVOLDOWN":     
                i=i+1
                #n[i] = n[i]+1
                sendCommand.wait_for_output(shell, olt[3], "config\n", "#")
                sendCommand.wait_for_output(shell, olt[3], "terminal length 0\n", "#")
                output = sendCommand.wait_for_output(shell, olt[3], "show hcu card\n", "#")
                #shell.send(command + "\n")
                #time.sleep(2)
                #time.sleep(2)
                print(output)
                match = re.search(r"total_load_current = (\d+\.\d+)", str(output))
                match2 = re.search(r"battery_capacity = (\d+\.\d+)", str(output))
                match3 = re.search(r"DC_voltage = (\d+\.\d+)", str(output))
                match4 = re.search(r"AC_voltage_R = (\d+\.\d+)", str(output))
                if match and match2 and match3:
                    bat_percentage = float(match2.group(1))  
                    current_load = str(match.group(1))
                    voltase = str(match3.group(1))
                    voltaseAC = str(match4.group(1))

                    print(current_load,bat_percentage,voltase)
                    #hitung sisa baterai
                    sisabaterai=bat_percentage*40
                    bat_percentage=str(bat_percentage)
                    sisabaterai=str(sisabaterai)
                    cursor = connection.cursor()
                    sekarang = datetime.now()
                    #print(sekarang)

                    #cek selisih waktu
                    waktu = sekarang.strftime("%Y-%m-%d %H:%M:%S")
                    lastcheck = 'select time from `test_dropvoltage` where `ip`="'+olt[0]+'";'
                    cursor.execute(lastcheck)
                    firsttime = cursor.fetchone()

                       
                    
                    #cek online user
                    outputonline = sendCommand.wait_for_output(shell, olt[3], "show onu auth-and-online statistics level system\n", "#")
                    onlinecheck =  'select online from `olt_onlineuser` where `ip`="'+olt[0]+'";'
                    cursor.execute(onlinecheck)
                    onlinecheck = cursor.fetchone()
                    #outputonline =shell.recv(65535)
                    print(outputonline)
                    outputonline=str(outputonline)
                    onlinematch = re.search(r"\d+/\d+ ", outputonline)  
                    if onlinematch:
                        if onlinecheck is None :
                            useronline = onlinematch.group(0)
                            useronline = str(useronline)
                            tableonline= 'INSERT INTO `olt_onlineuser`(`ip`, `hostname`, `online`) VALUES ("'+olt[0]+'","'+olt[3]+'","'+useronline+'");'
                            cursor.execute(tableonline)
                            connection.commit() 
                        useronline = onlinematch.group(0)
                        useronline = str(useronline)    
                        tableonline= 'UPDATE `olt_onlineuser` SET `online`="'+useronline+'" WHERE `ip`="'+olt[0]+'";'
                        cursor.execute(tableonline)
                        connection.commit()
                    
                    #cek apakah data baru dimasukkan pertama kali
                    if firsttime is None:
                        #cek lagi sudah hilang apa belum
                        doublecheck = 'select hostname from olt_warning where `ip`="'+olt[0]+'";'
                        cursor.execute(doublecheck)
                        checkWarning = cursor.fetchone() 

                        if checkWarning is not None:
                            elapsedsecond=0
                            elapsedsecond=str(elapsedsecond)
                            sql_insert_table_warning = 'INSERT INTO `test_dropvoltage`(`ip`,`voltage`,`current_load`,`Percentage`,`capacity`,`time`,`time_elapsed`) VALUES ("'+olt[0]+'","'+voltase+'","'+current_load+'","'+bat_percentage+'","'+sisabaterai+'","'+waktu+'","'+elapsedsecond+'");'
                            cursor.execute(sql_insert_table_warning)
                            connection.commit()
                            if float(voltaseAC) > 0:
                                firstingfo="listrik "+olt[3]+" tidak mati, voltase AC saat ini down, sebesar: "+ voltaseAC+" V"
                            else:
                                firstingfo="STATUS "+olt[3]+" : VOLTASE DC = " + voltase + " | VOLTASE AC = " + voltaseAC + " | ARUS BEBAN = " +current_load+" | ONLINE USER = "+useronline
                            #bot.send_message(-1001851139717,firstingfo)
                            msg_maingroup = url_maingroup+firstingfo
                            requests.get(msg_maingroup)

                            #cek id grup
                            grupWitel = getGroupID.getID(connection,olt[0])
                            msg_grupWitel = grupWitel + firstingfo
                            requests.get(msg_grupWitel,timeout=5)

                            '''msg_mtcgroup = url_mtcgroup+firstingfo
                            requests.get(msg_mtcgroup)'''
                            n[i]=0
                            floorsec[i] = 0
                        else:
                            print("olt ", olt[3], " listrik sudah UP")
                    else :
                        #cek lagi sudah hilang apa belum
                        doublecheck = 'select hostname from olt_warning where `ip`="'+olt[0]+'";'
                        cursor.execute(doublecheck)
                        checkWarning = cursor.fetchone()
                        if checkWarning is not None:
                            #print(firsttime[0])
                            datetime_object = datetime.strptime(firsttime[0], '%Y-%m-%d %H:%M:%S')
                            timeelapsed = sekarang - datetime_object
                            
                            elapsedsecond = timeelapsed.total_seconds() #%86400
                            floorsec[i] = mt.floor(elapsedsecond/1800)
                            elapsedsecond = str(elapsedsecond)
                            sql_insert_table_warning = 'INSERT INTO `test_dropvoltage`(`ip`,`voltage`,`current_load`,`Percentage`,`capacity`,`time`,`time_elapsed`) VALUES ("'+olt[0]+'","'+voltase+'","'+current_load+'","'+bat_percentage+'","'+sisabaterai+'","'+waktu+'","'+elapsedsecond+'");'
                            #sql_update_table = 'UPDATE test_dropvoltage SET time_elapsed = UNIX_TIMESTAMP(time) - (SELECT UNIX_TIMESTAMP(MIN(time)) FROM test_dropvoltage);'
                            cursor.execute(sql_insert_table_warning)
                            connection.commit()
                else :
                    print("Tidak dapat menemukan status baterai untuk OLT ", olt[0] )
                
                #Cek untuk melakukan training dan prediksi
                if floorsec[i] != n[i] and floorsec[i] !=0 :
                    n[i]=floorsec[i]
                    train.train(olt[0])
                    remaining, jatuhtempo = predict.predict(olt[0])
                    #remaining = remaining/3600
                    #remaining = str(remaining)
                    info = "Sisa waktu pada OLT "+olt[3]+" ("+olt[0]+") adalah: "+remaining+" dengan predikisi mati pada : "+jatuhtempo+" ( Voltase DC = "+voltase+" | Voltase AC = "+voltaseAC+" | Sisa baterai = "+bat_percentage+" | Beban Arus = " +current_load+" | Online User = "+useronline+" )"
                    #kirim = str(info)
                    #bot.send_message(-1001851139717,info)
                    msg_maingroup = url_maingroup+info
                    requests.get(msg_maingroup,timeout=5)

                    #cek id grup
                    grupWitel = getGroupID.getID(connection,olt[0])
                    msg_grupWitel = grupWitel + info
                    requests.get(msg_grupWitel,timeout=5)
                    '''msg_mtcgroup = url_mtcgroup+info
                    requests.get(msg_mtcgroup)'''
                    #mess= url_maingroup+str(info)
                    #requests.get(mess)
                    print("Sisa waktu pada OLT "+olt[3]+" ("+olt[0]+") adalah: "+remaining+" jam ,( Voltase = "+voltase+" | Sisa baterai = "+bat_percentage+" | Beban Arus = " +current_load)
            else :
                print("Skipped "+olt[3]+" karena tidak discharging")
         
    ssh.close


schedule.every(1).seconds.do(func)

while True: 
    schedule.run_pending()
    time.sleep(0.1)
#    time.sleep(5)