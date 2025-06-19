import paramiko
import time
import schedule
import pymysql  
import re

connection = pymysql.connect(host='127.0.0.1',user='root',password='',db='tesoltkp')
cursor = connection.cursor()
sql_list = 'select ip, versi, hostname, posisi,merk from olt_list;'
cursor.execute(sql_list)
data = cursor.fetchall()

#ip, user, password telnet
ip_address = "10.60.190.16"
usr = "940305"
pwd = "Ilfannafli01"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=ip_address, username=usr, password=pwd)
time.sleep(3)
print("SSH connection is successfully established with ", ip_address)

def func():
    for olt in data:
        shell = ssh.invoke_shell()
            
        #cek ping dulu baru lanjut telnet
        testping = shell.recv(65535)
        shell.send("ping "+olt[0]+" -c 2\n")
        time.sleep(3)
        testping = shell.recv(65535)

        print(olt[0])
        shell.send("telnet "+olt[0]+"\n")
        time.sleep(3)
        ceklogin = shell.recv(65535)
        shell.send(usr + "\n")
        cekusr = shell.recv(65535)

        shell.send(pwd + "\n")
        cekpwd = shell.recv(65535)
        
        time.sleep(5)

        #command list untuk OLT versi AN5516-04
        if olt[1] == "AN5516-04": 
            cmd2 = ["cd device",
                    "show hcu env_para card"]   
                        
            for command2 in cmd2:
                shell.send(command2 + "\n")  
                if command2 == "show hcu env_para card"  :
                    shell.send(command2 + "\n")    
                    time.sleep(3)         
                output2= shell.recv(65535)
                output2 = output2.decode()
                match = re.search(r"total_load_current (\d+\.\d+)", output2)
                current_load = float(match.group(1))

        if olt[1] == "AN6000-2": 
                cmd2 = ["config",
                        "show hcu card"]
                for command2 in cmd2:
                    shell.send(command2 + "\n")  
                    if command2 == "show hcu card"  :
                        shell.send("clear"+"\n")
                        shell.send(command2 + "\n")    
                        time.sleep(3)         
                    output2= shell.recv(65535)
                    output2 = output2.decode()
                    match = re.search(r"total_load_current (\d+\.\d+)", output2)
                    current_load = float(match.group(1)) 
                    match2 = re.search(r"battery_capacity (\d+\.\d+)", output2)
                    bat_percentage = float(match2.group(1))

        sisabaterai=bat_percentage*40
        cursor = connection.cursor()
        sql_insert_table_warning = 'INSERT INTO `test_dropvoltage`(`ip`,`voltage`,`current_load`,`Percentage`,`capacity`) VALUES ("'+olt[0]+'","'+0+'","'+current_load+'","'+bat_percentage+'","'+sisabaterai+'");'
        cursor.execute(sql_insert_table_warning)
        connection.commit()
        
        ssh.close 

schedule.every(5).seconds.do(func)

while True: 
    schedule.run_pending()
#    time.sleep(5)