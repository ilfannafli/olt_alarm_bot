import paramiko
import time
import requests
import schedule
import pymysql  
import datetime
from checkfunc import CheckOLTVersion as OLTVer
from checkfunc import CekPosOLT
from checkfunc import CheckMiniOLTFiberHome
from checkfunc import cekonlineuser
from getfunc import getGeneralData
from getfunc import getPIC
from getfunc import getListOLT
from getfunc import getIPMO
from getfunc import getIPMOdr
from getfunc import getLoginData
from checkfunc import sendCommand
import os
threadke='8'
connection = pymysql.connect(host='localhost',user='root',password='',db='testoltkp')
cursor = connection.cursor()
sql_list = 'select ip, versi, hostname, posisi,merk from olt_list where thread='+threadke+';'
cursor.execute(sql_list)
data = cursor.fetchall()
pid = os.getpid()
with open("pid_thread8.txt", "w") as file:
    file.write(str(pid)) 


url_maingroup,url_mtcgroup,url_kpgroup, url_patroligroup, ip_address,usr,pwd = getLoginData.custom(connection)
#alamat grup Telegram
#url_maingroup = 'https://api.telegram.org/bot5955267891:AAHCHgC3K2x4xMMSbDtN6FVrXojkD0EqyDE/sendMessage?chat_id=-1001851139717&text='
#url_mtcgroup = 'https://api.telegram.org/bot5933357528:AAGoECge8eGvPFQqG3Y1xfXeA3-yu-tVy8Q/sendMessage?chat_id=-865403076&text='
#url_maingroup = 'https://api.telegram.org/bot5933357528:AAGoECge8eGvPFQqG3Y1xfXeA3-yu-tVy8Q/sendMessage?chat_id=-1001851139717&text='
#url_mtcgroup = 'https://api.telegram.org/bot5933357528:AAGoECge8eGvPFQqG3Y1xfXeA3-yu-tVy8Q/sendMessage?chat_id=-1001851139717&text='

#ip, user, password telnet
#ip_address = "10.60.190.16"
#usr = "940305"
#pwd = "Ilfannafli01"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=ip_address, username=usr, password=pwd)

print("SSH connection is successfully established with ", ip_address)
time.sleep(3)

def func():
    for olt in data :
        #ip_address = "10.60.190.16"
        #usr = "940305"
        #pwd = "Ilfannafli01"

        #ssh = paramiko.SSHClient()
        #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #ssh.connect(hostname=ip_address, username=usr, password=pwd)
        #print("SSH connection is successfully established with ", ip_address)
        #time.sleep(0.2)
        shell = ssh.invoke_shell()
        testping = sendCommand.wait_for_output(shell, olt[2], "ping "+olt[0]+" -c 2\n", "packets")
        ceklogin = sendCommand.wait_for_output(shell, olt[2], "telnet "+olt[0]+"\n", "Login")
        sendCommand.wait_for_output(shell, olt[2], usr + "\n", "Password")
        sendCommand.wait_for_output(shell, olt[2], pwd + "\n", "#") 
        print(olt[2])
            
        #Command Check Versi OLT
        output = OLTVer.CheckOLTVersion(olt[1],shell,olt[2])
        #print(output.decode())
        #print(cmd)
        #Command cekonlineuser
        onlinematch = cekonlineuser.user(olt[1],shell,olt[2])
        #ambil ip MO
        mo_warning = getIPMO.IPMO(olt[0],connection)
        
        mo_door =getIPMOdr.IPMOdr(olt[0],connection)

        #ambil list olt down
        mo_down = getListOLT.mo_down(olt[0],connection)
         
        #ambil data pic
        #pic= getPIC.PIC(olt[0],connection)

        #cek OLT INDOOR dan MSAN
        CekPosOLT.cekpos(olt[3],olt[4],olt[0],olt[2],ceklogin,testping,mo_down,connection,url_mtcgroup,url_maingroup)

        #cek Mini OLT FiberHome
        #print(output.decode())
        CheckMiniOLTFiberHome.MiniOLTcheck(olt[0],olt[2],olt[1],mo_warning,mo_down,testping,url_maingroup,url_mtcgroup,url_kpgroup,url_patroligroup,connection,ceklogin,output,onlinematch,mo_door)
        time.sleep(1)
        ssh.close 
  
schedule.every(1).seconds.do(func)

while True: 
    schedule.run_pending()
#    time.sleep(5)