import paramiko
import time
import requests
import schedule
import pymysql  
import datetime
from concurrent.futures import ThreadPoolExecutor
from checkfunc import CheckOLTVersion as OLTVer
from checkfunc import CekPosOLT
from checkfunc import CheckMiniOLTFiberHome
from getfunc import getGeneralData
from getfunc import getPIC
from getfunc import getListOLT
from getfunc import getIPMO
from getfunc import getIPMOdr
from getfunc import getLoginData
connection = pymysql.connect(host='127.0.0.1',user='root',password='',db='tesoltkp')
cursor = connection.cursor()
sql_list = 'select ip, versi, hostname, posisi,merk from olt_list;'
cursor.execute(sql_list)
data = cursor.fetchall()

url_maingroup,url_mtcgroup,url_kpgroup, ip_address,usr,pwd = getLoginData.custom()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=ip_address, username=usr, password=pwd)

print("SSH connection is successfully established with ", ip_address)
start = time.process_time()
olt = ['172.29.238.202' ,'AN6000-2', 'GPON00-D4-WOS-4FAN','OUTDOOR','FIBERHOME']
    # code for each thread goes here
#olt[0]="172.29.238.250"
shell = ssh.invoke_shell()
    
#cek ping dulu baru lanjut telnet
testping = shell.recv(65535)
shell.send("ping "+olt[0]+" -c 2\n")
time.sleep(2)
testping = shell.recv(65535)
#print(testping.decode())
print(olt[0])
shell.send("telnet "+olt[0]+"\n")
time.sleep(2)
ceklogin = shell.recv(65535)
#print(ceklogin.decode())
shell.send(usr + "\n")
cekusr = shell.recv(65535)
print(cekusr.decode())
shell.send(pwd + "\n")
cekpwd = shell.recv(65535)
#print(cekpwd.decode())
time.sleep(2)
print(cekpwd.decode())
    
#Command Check Versi OLT
output = OLTVer.CheckOLTVersion(olt[1],shell)
print(output.decode())
#print(cmd)

#ambil ip MO
mo_warning = getIPMO.IPMO(olt[0],connection)

#ambil list olt down
mo_down = getListOLT.mo_down(olt[0],connection)

mo_door =getIPMOdr.IPMOdr(olt[0],connection)
 
#ambil data pic
pic= getPIC.PIC(olt[0],connection)
print(pic)
#ambil data general check up
voltase= getGeneralData.voltase(olt[0],connection)

#cek OLT INDOOR dan MSAN
CekPosOLT.cekpos(olt[3],olt[4],olt[0],olt[2],ceklogin,testping,mo_down,connection,url_mtcgroup,url_maingroup,pic)

#cek Mini OLT FiberHome
#print(output.decode())
CheckMiniOLTFiberHome.MiniOLTcheck(olt[0],olt[2],olt[1],mo_warning,mo_down,testping,url_maingroup,url_mtcgroup,url_kpgroup,connection,pic,ceklogin,output,voltase,mo_door)
ssh.close