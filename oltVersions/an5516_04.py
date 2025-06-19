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

def AN5516_04(connection,shell,olt0):
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
                waktu = sekarang.strftime("%Y-%m-%d %H:%M:%S")
                lastcheck =  'select time from `test_dropvoltage` where `ip`="'+olt0+'";'
                cursor.execute(lastcheck)
                firsttime = cursor.fetchone()        
                
                #cek online user
                shell.send("cd /" + "\n")
                shell.send("cd onu" + "\n")
                shell.send("show onu auth-and-online statistics level system" +"\n")
                time.sleep(2)
                onlinecheck =  'select online from `olt_onlineuser` where `ip`="'+olt0+'";'
                cursor.execute(onlinecheck)
                onlinecheck = cursor.fetchone()
                outputonline =shell.recv(65535)
                print(outputonline.decode())
                outputonline=str(outputonline)
                onlinematch = re.search(r"\d+/\d+ ", outputonline)  

                return sekarang,onlinematch,firsttime,cursor,onlinecheck,bat_percentage,current_load,voltase,sisabaterai,waktu