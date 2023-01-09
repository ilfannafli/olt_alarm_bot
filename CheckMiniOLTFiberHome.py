import paramiko
import time
import requests
import schedule
import pymysql  
import datetime

def MiniOLTcheck(olt0,olt2,mo_warning,mo_down,testping,url_maingroup,url_mtcgroup,connection,pic,ceklogin,output,voltase) :
        if "Login" not in str(ceklogin):
            if "ttl" not in str(testping) and "ACVOLDOWN" not in str(mo_warning) and olt0 not in str(mo_down):

                cursor = connection.cursor()
                sql_insert_table_warning = 'INSERT INTO `olt_down`(`ip`,`status`) VALUES ("'+olt0+'","DOWN");'
                cursor.execute(sql_insert_table_warning)
                connection.commit()
                

                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","OLT DOWN","START","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()  

                msg_maingroup = url_maingroup+olt2+' ('+olt0+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'#+pic
                requests.get(msg_maingroup)
                msg_mtcgroup = url_mtcgroup+olt2+' ('+olt0+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'#+pic
                requests.get(msg_mtcgroup)                
                #print(olt0)


            elif "ACVOLDOWN" in str(mo_warning) and olt0 not in str(mo_down):
                
                cursor = connection.cursor()
                sql_insert_table_warning = 'INSERT INTO `olt_down`(`ip`,`status`) VALUES ("'+olt0+'","DOWN");'
                cursor.execute(sql_insert_table_warning)
                connection.commit()   
                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","OLT DOWN","START","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()
                
                """cursor = connection.cursor()
                sql_delete_table_warning = 'DELETE FROM `olt_warning` WHERE ip="'+olt0+'";'
                cursor.execute(sql_delete_table_warning)
                connection.commit()"""
            
                msg_maingroup = url_maingroup+"Baterai "+olt2+' ('+olt0+') telah habis.\nMini OLT DOWN\n'+pic
                msg_mtcgroup = url_mtcgroup+"Baterai "+olt2+' ('+olt0+') telah habis.\nMini OLT DOWN\n'+pic
                requests.get(msg_maingroup)
                requests.get(msg_mtcgroup)
                #print(olt0)

            elif "ttl" not in str(testping) and olt0 not in str(mo_down):
                cursor = connection.cursor()
                sql_insert_table_warning = 'INSERT INTO `olt_down`(`ip`,`status`) VALUES ("'+olt0+'","LOS");'
                cursor.execute(sql_insert_table_warning)
                connection.commit()   
                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","OLT LOS","START","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()

                msg_maingroup = url_maingroup+olt2+' ('+olt0+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'#+pic
                requests.get(msg_maingroup)
                msg_mtcgroup = url_mtcgroup+olt2+' ('+olt0+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'#+pic
                requests.get(msg_mtcgroup)                
                print(olt0)
        else:
            if olt0 in str(mo_down):
                cursor = connection.cursor()
                sql_delete_table_warning = 'DELETE FROM `olt_down` WHERE ip="'+olt0+'";'
                cursor.execute(sql_delete_table_warning)
                connection.commit()

                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","OLT DOWN","END","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()                         

            if "ACVOLDOWN" in str(output) and olt0 not in str(mo_warning):            
                cursor = connection.cursor()
                sql_insert_table_warning = 'INSERT INTO `olt_warning`(`ip`,`status`) VALUES ("'+olt0+'","ACVOLDOWN");'
                cursor.execute(sql_insert_table_warning)
                connection.commit()   

                ct = datetime.datetime.now()
                cursor = connection.cursor()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","ACVOLDOWN","START","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()  

                msg_maingroup = url_maingroup+olt2+' ('+olt0+') Terdeteksi mati listrik, power saat ini disupply dengan baterai.\nHasil assessment OLT bertahan >2 jam, dengan voltase setelah 2 jam '+voltase+' \nHarap lakukan pengecekan PLN terkait pemadaman listrik atau power di Mini OLT.\n'+pic
                requests.get(msg_maingroup)
                msg_mtcgroup = url_mtcgroup+olt2+' ('+olt0+') Terdeteksi mati listrik, power saat ini disupply dengan baterai.\nHasil assessment OLT bertahan >2 jam, dengan voltase setelah 2 jam '+voltase+' \nHarap lakukan pengecekan PLN terkait pemadaman listrik atau power di Mini OLT.\n'+pic
                requests.get(msg_mtcgroup)                
                #print(olt0)


            if "ACVOLDOWN" not in str(output) and olt0 in str(mo_warning):             
                cursor = connection.cursor()
                sql_delete_table_warning = 'DELETE FROM `olt_warning` WHERE ip="'+olt0+'";'
                cursor.execute(sql_delete_table_warning)
                connection.commit()     

                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","ACVOLDOWN","END","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()           

                msg_maingroup = url_maingroup+olt2+' ('+olt0+') Listrik sudah menyala'
                requests.get(msg_maingroup)
                msg_mtcgroup = url_mtcgroup+olt2+' ('+olt0+') Listrik sudah menyala'
                requests.get(msg_mtcgroup)
                #print(olt0)

            if "ttl" in str(testping) and olt0 in str(mo_down):
                cursor = connection.cursor()
                sql_delete_table_warning = 'DELETE FROM `olt_warning` WHERE ip="'+olt0+'";'
                cursor.execute(sql_delete_table_warning)
                connection.commit()

                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","OLT LOS","END","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()

                msg_maingroup = url_maingroup+olt2+' ('+olt0+') sudah UP.'
                requests.get(msg_maingroup)
                msg_mtcgroup = url_mtcgroup+olt2+' ('+olt0+') sudah UP.'
                requests.get(msg_mtcgroup)                
                print(olt0)
