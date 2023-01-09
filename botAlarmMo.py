import paramiko
import time
import requests
import schedule
import pymysql  
import datetime
import CheckOLTVersion as OLTVer
import CekPosOLT
import getGeneralData
import getPIC
import getListOLT
import getIPMO

connection = pymysql.connect(host='127.0.0.1',user='root',password='',db='alarm_olt')
cursor = connection.cursor()
sql_list = 'select ip, versi, hostname, posisi,merk from olt_list;'
cursor.execute(sql_list)
data = cursor.fetchall()


#alamat grup Telegram
url_maingroup = 'https://api.telegram.org/bot[API BOT]/sendMessage?chat_id=[id grup telegram]&text='
url_mtcgroup = 'https://api.telegram.org/bot[API BOT]/sendMessage?chat_id=[id grup telegram]&text='

#ip, user, password telnet
ip_address = "[xxxxxx]"
usr = "[xxxxxx]"
pwd = "[xxxxxx]"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=ip_address, username=usr, password=pwd)

print("SSH connection is successfully established with ", ip_address)

def func():
    for olt in data :
        shell = ssh.invoke_shell()
        
        #cek ping dulu baru lanjut telnet
        testping = shell.recv(65535)
        shell.send("ping "+olt[0]+" -c 2\n")
        time.sleep(3)
        testping = shell.recv(65535)
        print(testping.decode())
        print(olt[0])
        shell.send("telnet "+olt[0]+"\n")
        time.sleep(3)
        ceklogin = shell.recv(65535)
        print(ceklogin.decode())
        shell.send(usr + "\n")
        cekusr = shell.recv(65535)
        print(cekusr.decode())
        shell.send(pwd + "\n")
        cekpwd = shell.recv(65535)
        print(cekpwd.decode())
        time.sleep(3)
        
        #Command Check Versi OLT
        output = OLTVer.CheckOLTVersion(olt[1])
          
        #print(cmd)

        #ambil ip MO
        getIPMO.IPMO(olt[0])

        #ambil list olt down
        getListOlt.ListOLT(olt[0])
     

        #ambil data pic
        pic= getPIC.PIC(olt[0])

        #ambil data general check up
        voltase= getGeneralData.general(olt[0])

        #cek OLT INDOOR dan MSAN
        CekPosOLT.cekpos(olt[3],olt[4],olt[0],olt[2])

        #cek Mini OLT FiberHome
        #print(output.decode())
        if "Login" not in str(ceklogin):
            if "ttl" not in str(testping) and "ACVOLDOWN" not in str(mo_warning) and olt[0] not in str(mo_down):

                cursor = connection.cursor()
                sql_insert_table_warning = 'INSERT INTO `olt_down`(`ip`,`status`) VALUES ("'+olt[0]+'","DOWN");'
                cursor.execute(sql_insert_table_warning)
                connection.commit()
                

                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt[0]+'","OLT DOWN","START","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()  

                msg_maingroup = url_maingroup+olt[2]+' ('+olt[0]+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'#+pic
                requests.get(msg_maingroup)
                msg_mtcgroup = url_mtcgroup+olt[2]+' ('+olt[0]+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'#+pic
                requests.get(msg_mtcgroup)                
                #print(olt[0])


            elif "ACVOLDOWN" in str(mo_warning) and olt[0] not in str(mo_down):
                
                cursor = connection.cursor()
                sql_insert_table_warning = 'INSERT INTO `olt_down`(`ip`,`status`) VALUES ("'+olt[0]+'","DOWN");'
                cursor.execute(sql_insert_table_warning)
                connection.commit()   
                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt[0]+'","OLT DOWN","START","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()
                
                """cursor = connection.cursor()
                sql_delete_table_warning = 'DELETE FROM `olt_warning` WHERE ip="'+olt[0]+'";'
                cursor.execute(sql_delete_table_warning)
                connection.commit()"""
            
                msg_maingroup = url_maingroup+"Baterai "+olt[2]+' ('+olt[0]+') telah habis.\nMini OLT DOWN\n'+pic
                msg_mtcgroup = url_mtcgroup+"Baterai "+olt[2]+' ('+olt[0]+') telah habis.\nMini OLT DOWN\n'+pic
                requests.get(msg_maingroup)
                requests.get(msg_mtcgroup)
                #print(olt[0])

            elif "ttl" not in str(testping) and olt[0] not in str(mo_down):
                cursor = connection.cursor()
                sql_insert_table_warning = 'INSERT INTO `olt_down`(`ip`,`status`) VALUES ("'+olt[0]+'","LOS");'
                cursor.execute(sql_insert_table_warning)
                connection.commit()   
                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt[0]+'","OLT LOS","START","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()

                msg_maingroup = url_maingroup+olt[2]+' ('+olt[0]+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'#+pic
                requests.get(msg_maingroup)
                msg_mtcgroup = url_mtcgroup+olt[2]+' ('+olt[0]+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'#+pic
                requests.get(msg_mtcgroup)                
                print(olt[0])
        else:
            if olt[0] in str(mo_down):
                cursor = connection.cursor()
                sql_delete_table_warning = 'DELETE FROM `olt_down` WHERE ip="'+olt[0]+'";'
                cursor.execute(sql_delete_table_warning)
                connection.commit()

                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt[0]+'","OLT DOWN","END","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()                         

            if "ACVOLDOWN" in str(output) and olt[0] not in str(mo_warning):            
                cursor = connection.cursor()
                sql_insert_table_warning = 'INSERT INTO `olt_warning`(`ip`,`status`) VALUES ("'+olt[0]+'","ACVOLDOWN");'
                cursor.execute(sql_insert_table_warning)
                connection.commit()   

                ct = datetime.datetime.now()
                cursor = connection.cursor()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt[0]+'","ACVOLDOWN","START","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()  

                msg_maingroup = url_maingroup+olt[2]+' ('+olt[0]+') Terdeteksi mati listrik, power saat ini disupply dengan baterai.\nHasil assessment OLT bertahan >2 jam, dengan voltase setelah 2 jam '+voltase+' \nHarap lakukan pengecekan PLN terkait pemadaman listrik atau power di Mini OLT.\n'+pic
                requests.get(msg_maingroup)
                msg_mtcgroup = url_mtcgroup+olt[2]+' ('+olt[0]+') Terdeteksi mati listrik, power saat ini disupply dengan baterai.\nHasil assessment OLT bertahan >2 jam, dengan voltase setelah 2 jam '+voltase+' \nHarap lakukan pengecekan PLN terkait pemadaman listrik atau power di Mini OLT.\n'+pic
                requests.get(msg_mtcgroup)                
                #print(olt[0])


            if "ACVOLDOWN" not in str(output) and olt[0] in str(mo_warning):             
                cursor = connection.cursor()
                sql_delete_table_warning = 'DELETE FROM `olt_warning` WHERE ip="'+olt[0]+'";'
                cursor.execute(sql_delete_table_warning)
                connection.commit()     

                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt[0]+'","ACVOLDOWN","END","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()           

                msg_maingroup = url_maingroup+olt[2]+' ('+olt[0]+') Listrik sudah menyala'
                requests.get(msg_maingroup)
                msg_mtcgroup = url_mtcgroup+olt[2]+' ('+olt[0]+') Listrik sudah menyala'
                requests.get(msg_mtcgroup)
                #print(olt[0])

            if "ttl" in str(testping) and olt[0] in str(mo_down):
                cursor = connection.cursor()
                sql_delete_table_warning = 'DELETE FROM `olt_warning` WHERE ip="'+olt[0]+'";'
                cursor.execute(sql_delete_table_warning)
                connection.commit()

                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt[0]+'","OLT LOS","END","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()

                msg_maingroup = url_maingroup+olt[2]+' ('+olt[0]+') sudah UP.'
                requests.get(msg_maingroup)
                msg_mtcgroup = url_mtcgroup+olt[2]+' ('+olt[0]+') sudah UP.'
                requests.get(msg_mtcgroup)                
                print(olt[0])

                
        ssh.close 
  
schedule.every(5).seconds.do(func)

while True: 
    schedule.run_pending()
#    time.sleep(5)