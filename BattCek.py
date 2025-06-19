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
from getfunc import getLoginData
import os
from BatteryFunctions import InputOnlineUsr,UpdateData,FirstData,TrainPredict
from oltVersions import an6000_2, an5516_04
pid = os.getpid()
with open("pid_battery.txt", "w") as file:
    file.write(str(pid)) 


bot = telebot.TeleBot('8108321673:AAGMkFTivNWOirWfL3qh2pDVao2tLhohadA')

connection = pymysql.connect(host='127.0.0.1',user='root',password='',db='tesoltkp')
url_maingroup,url_mtcgroup,url_kpgroup,ip_address,usr,pwd = getLoginData.custom(connection)

n=[0,0,0,0,0,0,0,0,0]
floorsec=[0,0,0,0,0,0,0,0,0]
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=ip_address, username=usr, password=pwd)

print("SSH connection is successfully established with ", ip_address)
start=datetime.time
    
 
def func():
    global n
    global floorsec
    i=0
    connection = pymysql.connect(host='localhost',user='root',password='',db='testoltkp')
    cursor = connection.cursor()
    data=()
    sql_list = 'select ip,versi, status, hostname from olt_warning;'
    cursor.execute(sql_list)
    data = cursor.fetchall()
    print(len(data))

    if len(data) == 0 : 
            print("Tidak ada OLT dalam status warning, menghapus query drop voltage\n")
            delete_query= 'DELETE FROM test_dropvoltage'
            delete_onlineuser='DELETE FROM olt_onlineuser'
            cursor.execute(delete_query)
            connection.commit()
            cursor.execute(delete_onlineuser)
            connection.commit()
            time.sleep(0.2)
            n=[0,0,0,0,0,0,0,0,0]
            floorsec=[0,0,0,0,0,0,0,0,0]
            print("Berhasil menghapus tabel lama")

    else : 
        for olt in data :
            current_load = 1
            bat_percentage = 1
            voltase = 1 
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
        
            if olt[1] == "AN5516-04" and olt[2] =="ACVOLDOWN" : 
                i=i+1
                #Output untuk versi AN5516-04
                sekarang,onlinematch,firsttime,cursor,onlinecheck,bat_percentage,current_load,voltase,sisabaterai,waktu = an5516_04.AN5516_04(connection,shell,olt[0])
                #input onlineuser ke db
                useronline =InputOnlineUsr.IOU(onlinematch,onlinecheck,olt[0],olt[3],cursor,connection)
                    
                #cek apakah data baru dimasukkan pertama kali    
                if firsttime is None :
                    FirstData.fd(olt[0],olt[3],voltase,bat_percentage,current_load,useronline,url_maingroup,url_mtcgroup,url_kpgroup,cursor,connection,sisabaterai,waktu)
                    n[i]=0
                    floorsec[i] = 0
                else :
                    floorsec[i] = UpdateData.UD(olt[0],firsttime[0],floorsec[i],voltase,bat_percentage,current_load,cursor,connection,sisabaterai,waktu,sekarang)
            
                    
                    #Cek untuk melakukan training dan prediksi
                    if floorsec[i] != n[i] and floorsec[i] !=0 :
                        n[i]=floorsec[i]
                        TrainPredict.TP(olt[0],olt[3],voltase,bat_percentage,current_load,useronline,url_maingroup,url_mtcgroup,url_kpgroup)                      
                    
                #command list untuk OLT versi AN6000-2           
            if olt[1] == "AN6000-2" and olt[2] == "ACVOLDOWN": 
                i=i+1
                #Output untuk versi AN6000-2
                sekarang,onlinematch,firsttime,cursor,onlinecheck,bat_percentage,current_load,voltase,sisabaterai,waktu = an6000_2.AN6000_2(connection,shell,olt[0])
                #input onlineuser ke db
                useronline = InputOnlineUsr.IOU(onlinematch,onlinecheck,olt[0],olt[3],cursor,connection)

                #cek apakah data baru dimasukkan pertama kali
                if firsttime is None :
                    FirstData.fd(olt[0],olt[3],voltase,bat_percentage,current_load,useronline,url_maingroup,url_mtcgroup,url_kpgroup,cursor,connection,sisabaterai,waktu)
                    n[i]=0
                    floorsec[i] = 0
                else :
                    floorsec[i] = UpdateData.UD(olt[0],firsttime[0],floorsec[i],voltase,bat_percentage,current_load,cursor,connection,sisabaterai,waktu,sekarang)
        
                    #Cek untuk melakukan training dan prediksi
                    if floorsec[i] != n[i] and floorsec[i] !=0 :
                        n[i]=floorsec[i]
                        TrainPredict.TP(olt[0],olt[3],voltase,bat_percentage,current_load,useronline,url_maingroup,url_mtcgroup,url_kpgroup)
            else :
                print("Skipped "+olt[0]+" karena tidak discharging")
         
    ssh.close


schedule.every(1).seconds.do(func)

while True: 
    schedule.run_pending()
    time.sleep(0.1)