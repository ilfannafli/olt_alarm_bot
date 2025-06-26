import paramiko
import time
import requests
import schedule
import pymysql  
import datetime
import telebot
from getfunc import getLoginData, getGroupID
bot = telebot.TeleBot('8108321673:AAGMkFTivNWOirWfL3qh2pDVao2tLhohadA')

def MiniOLTcheck(olt0,olt2,olt1,mo_warning,mo_down,testping,url_maingroup,url_mtcgroup,url_kpgroup,url_patroligroup,connection,ceklogin,output,onlinematch,mo_door) :
        #print("masuk MINIOLTCHECK untuk olt ", olt2)
        #bot.send_message(-1001851139717,"Berhasil Masuk MiniOLTcheck")
        if "Login" not in str(ceklogin):
            if "ttl" not in str(testping) and "ACVOLDOWN" not in str(mo_warning) and olt0 not in str(mo_down):

                cursor = connection.cursor()
                sql_insert_table_warning = 'INSERT INTO `olt_down`(`ip`,`status`,`versi`) VALUES ("'+olt0+'","DOWN","'+olt1+'");'
                cursor.execute(sql_insert_table_warning)
                connection.commit()
                

                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","OLT DOWN","START","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()  

                #cek id grup
                grupWitel = getGroupID.getID(connection,olt0)
                msg_grupWitel = grupWitel + olt2+' ('+olt0+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'
                requests.get(msg_grupWitel,timeout=5)

                msg_maingroup = url_maingroup+olt2+' ('+olt0+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'
                requests.get(msg_maingroup)
                #msg_mtcgroup = url_mtcgroup+olt2+' ('+olt0+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'
                #requests.get(msg_mtcgroup)                
                #print(olt0)
                
            #elif "ttl" not in str(testping) and "ACVOLDOWN" not in str(mo_warning) and olt0 in str(mo_down):

                #msg_maingroup = url_maingroup+olt2+' ('+olt0+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'
               # requests.get(msg_maingroup)
                #msg_mtcgroup = url_mtcgroup+olt2+' ('+olt0+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'
                #requests.get(msg_mtcgroup)                
                #print(olt0)

            elif "ttl" not in str(testping) and "BATTERY_MISSING" in str(mo_warning) and olt0 not in str(mo_down):
                
                cursor = connection.cursor()
                sql_insert_table_warning = 'INSERT INTO `olt_down`(`ip`,`status`,`versi`) VALUES ("'+olt0+'","DOWN_BATMISS","'+olt1+'");'
                cursor.execute(sql_insert_table_warning)
                connection.commit()   
                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","OLT DOWN BAT MISSING","START","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()
                msg_maingroup = url_maingroup+olt2+' ('+olt0+') Tidak terdapat baterai dan saat ini tidak tersuplai listrik'
                #msg_mtcgroup = url_mtcgroup+"Baterai "+olt2+' ('+olt0+') Tidak terdapat baterai dan saat ini tidak tersuplai listrik'
                requests.get(msg_maingroup)
                #requests.get(msg_mtcgroup)
                
            elif "ttl" not in str(testping) and "ACVOLDOWN" in str(mo_warning) and olt0 not in str(mo_down):
                
                cursor = connection.cursor()
                sql_insert_table_warning = 'INSERT INTO `olt_down`(`ip`,`status`,`versi`) VALUES ("'+olt0+'","DOWN","'+olt1+'");'
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
                #cek id grup
                grupWitel = getGroupID.getID(connection,olt0)
                msg_grupWitel = grupWitel + "Baterai "+olt2+' ('+olt0+') telah habis.\nMini OLT DOWN\n'
                requests.get(msg_grupWitel,timeout=5)

                msg_maingroup = url_maingroup+"Baterai "+olt2+' ('+olt0+') telah habis.\nMini OLT DOWN\n'
                #msg_mtcgroup = url_mtcgroup+"Baterai "+olt2+' ('+olt0+') telah habis.\nMini OLT DOWN\n'
                requests.get(msg_maingroup)
                #requests.get(msg_mtcgroup)
                #print(olt0)

            '''elif "ttl" not in str(testping) and olt0 not in str(mo_down):
                cursor = connection.cursor()
                sql_insert_table_warning = 'INSERT INTO `olt_down`(`ip`,`status`,`versi`) VALUES ("'+olt0+'","LOS","'+olt1+'");'
                cursor.execute(sql_insert_table_warning)
                connection.commit()   
                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","OLT LOS","START","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()'''
             
            '''elif "ttl" not in str(testping) and olt0 in str(mo_down) and "LOS" in str(mo_down):
                cursor = connection.cursor()
                sql_insert_table_warning = 'UPDATE `olt_down` SET `ip`="'+olt0+'",`status`="LSR" WHERE `ip`="'+olt0+'";'
                cursor.execute(sql_insert_table_warning)
                connection.commit()
                msg_maingroup = url_maingroup+olt2+' ('+olt0+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'
                requests.get(msg_maingroup)
                msg_mtcgroup = url_mtcgroup+olt2+' ('+olt0+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'
                requests.get(msg_mtcgroup)
                msg_kpgroup = url_kpgroup+olt2+' ('+olt0+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'
                requests.get(msg_kpgroup) 
                print(olt0)'''
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

                #cek id grup
                grupWitel = getGroupID.getID(connection,olt0)
                msg_grupWitel = grupWitel + olt2+' ('+olt0+') sudah UP.'
                requests.get(msg_grupWitel,timeout=5)

                msg_maingroup = url_maingroup+olt2+' ('+olt0+') sudah UP.'
                requests.get(msg_maingroup)                 

            if "ACVOLDOWN" in str(output) and "Current Alarm" in str(output) and olt0 not in str(mo_warning):            
                cursor = connection.cursor()
                sql_insert_table_warning = 'INSERT INTO `olt_warning`(`ip`,`status`,`versi`,`hostname`) VALUES ("'+olt0+'","ACVOLDOWN","'+olt1+'","'+olt2+'");'
                cursor.execute(sql_insert_table_warning)
                connection.commit()   
                ct = datetime.datetime.now()
                cursor = connection.cursor()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","ACVOLDOWN","START","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()  

                
                msg_maingroup = url_maingroup+olt2+' ('+olt0+') Terdeteksi mati listrik, power saat ini disupply dengan baterai. \nHarap lakukan pengecekan PLN terkait pemadaman listrik atau power di Mini OLT.\n'
                requests.get(msg_maingroup)
                #msg_mtcgroup = url_mtcgroup+olt2+' ('+olt0+') Terdeteksi mati listrik, power saat ini disupply dengan baterai. \nHarap lakukan pengecekan PLN terkait pemadaman listrik atau power di Mini OLT.\n'
                #requests.get(msg_mtcgroup) 
                #print(olt0)
            
            '''if "AC_FAIL" in str(output) and "Current Alarm" in str(output) and olt0 not in str(mo_warning):            
                cursor = connection.cursor()
                sql_insert_table_warning = 'INSERT INTO `olt_warning`(`ip`,`status`,`versi`,`hostname`) VALUES ("'+olt0+'","ACVOLDOWN","'+olt1+'","'+olt2+'");'
                cursor.execute(sql_insert_table_warning)
                connection.commit()   
                ct = datetime.datetime.now()
                cursor = connection.cursor()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","ACVOLDOWN","START","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()  

                
                msg_maingroup = url_maingroup+olt2+' ('+olt0+') Terdeteksi mati listrik, power saat ini disupply dengan baterai. \nHarap lakukan pengecekan PLN terkait pemadaman listrik atau power di Mini OLT.\n'
                requests.get(msg_maingroup)
                msg_mtcgroup = url_mtcgroup+olt2+' ('+olt0+') Terdeteksi mati listrik, power saat ini disupply dengan baterai. \nHarap lakukan pengecekan PLN terkait pemadaman listrik atau power di Mini OLT.\n'
                requests.get(msg_mtcgroup)
                msg_kpgroup = url_kpgroup+olt2+' ('+olt0+') Terdeteksi mati listrik, power saat ini disupply dengan baterai. \nHarap lakukan pengecekan PLN terkait pemadaman listrik atau power di Mini OLT.\n'
                requests.get(msg_kpgroup)  
                #print(olt0)  ''' 
                
            if "BATTERY_MISSING" in str(output) and "Current Alarm" in str(output) and olt0 not in str(mo_warning):            
                cursor = connection.cursor()
                sql_insert_table_warning = 'INSERT INTO `olt_warning`(`ip`,`status`,`versi`,`hostname`) VALUES ("'+olt0+'","BATTERY_MISSING","'+olt1+'","'+olt2+'");'
                cursor.execute(sql_insert_table_warning)
                connection.commit()   
                ct = datetime.datetime.now()
                cursor = connection.cursor()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","BATTERY_MISSING","START","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit() 
                msg_maingroup = url_maingroup+olt2+' ('+olt0+') Terdeteksi tidak terpasang baterai\n'
                requests.get(msg_maingroup)
                #msg_mtcgroup = url_mtcgroup+olt2+' ('+olt0+') Terdeteksi tidak terpasang baterai\n'
                #requests.get(msg_mtcgroup)
                
            if "ACVOLDOWN" not in str(output) and "Current Alarm" in str(output) and olt0 in str(mo_warning) and "ACVOLDOWN" in str(mo_warning):             
                cursor = connection.cursor()
                sql_delete_table_warning = 'DELETE FROM `olt_warning` WHERE ip="'+olt0+'";'
                cursor.execute(sql_delete_table_warning)
                connection.commit()     

                delete_query= 'DELETE FROM test_dropvoltage WHERE ip="'+olt0+'";'
                cursor.execute(delete_query)
                connection.commit()
                
                delete_onlineuser='DELETE FROM olt_onlineuser WHERE ip="'+olt0+'";'
                cursor.execute(delete_onlineuser)
                connection.commit()
                print("Berhasil menghapus tabel lama")

                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","ACVOLDOWN","END","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()           

                #cek id grup
                grupWitel = getGroupID.getID(connection,olt0)
                msg_grupWitel = grupWitel + olt2+' ('+olt0+') Listrik sudah menyala'
                requests.get(msg_grupWitel,timeout=5)

                msg_maingroup = url_maingroup+olt2+' ('+olt0+') Listrik sudah menyala'
                requests.get(msg_maingroup)
                #msg_mtcgroup = url_mtcgroup+olt2+' ('+olt0+') Listrik sudah menyala'
                #requests.get(msg_mtcgroup)
                #print(olt0)
            
            if "BATTERY_MISSING" not in str(output) and "Current Alarm" in str(output) and olt0 in str(mo_warning) and "BATTERY_MISSING" in str(mo_warning):             
                cursor = connection.cursor()
                sql_delete_table_warning = 'DELETE FROM `olt_warning` WHERE ip="'+olt0+'";'
                cursor.execute(sql_delete_table_warning)
                connection.commit()     

                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","BATTERY_MISSING","END","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()           

                msg_maingroup = url_maingroup+olt2+' ('+olt0+') sudah terpasang baterai'
                requests.get(msg_maingroup)
                #msg_mtcgroup = url_mtcgroup+olt2+' ('+olt0+') sudah terpasang baterai'
                #requests.get(msg_mtcgroup)
                #print(olt0)
            
            if "ACVOLDOWN" not in str(output) and "Current Alarm" in str(output):
                cursor = connection.cursor()
                onlinecheck =  'select online from `olt_normalonline` where `ip`="'+olt0+'";'
                cursor.execute(onlinecheck)
                onlinecheck = cursor.fetchone()
                if onlinematch:
                    if onlinecheck is None :
                        useronline = onlinematch.group(0)
                        useronline = str(useronline)
                        tableonline= 'INSERT INTO `olt_normalonline`(`ip`, `hostname`, `online`) VALUES ("'+olt0+'","'+olt2+'","'+useronline+'");'
                        cursor.execute(tableonline)
                        connection.commit() 
                    useronline = onlinematch.group(0)
                    useronline = str(useronline)    
                    tableonline= 'UPDATE `olt_normalonline` SET `online`="'+useronline+'" WHERE `ip`="'+olt0+'";'
                    cursor.execute(tableonline)
                    connection.commit()    

            if "ttl" in str(testping) and olt0 in str(mo_down):
                cursor = connection.cursor()
                sql_delete_table_warning = 'DELETE FROM `olt_warning` WHERE ip="'+olt0+'";'
                cursor.execute(sql_delete_table_warning)
                connection.commit()

                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","OLT LOS","END","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()

                #cek id grup
                grupWitel = getGroupID.getID(connection,olt0)
                msg_grupWitel = grupWitel + olt2+' ('+olt0+') sudah UP.'
                requests.get(msg_grupWitel,timeout=5)

                msg_maingroup = url_maingroup+olt2+' ('+olt0+') sudah UP.'
                requests.get(msg_maingroup)
                #msg_mtcgroup = url_mtcgroup+olt2+' ('+olt0+') sudah UP.'
                #requests.get(msg_mtcgroup)               
                #print(olt0)
            
            if "Battery_bunker_door_alarm" in str(output) and "Current Alarm" in str(output) and "BUNKER_OPEN" not in str(mo_door):
                cursor = connection.cursor()
                sql_door_alarm = 'INSERT INTO `olt_warningdoor`(`ip`,`status`,`versi`) VALUES ("'+olt0+'","BUNKER_OPEN","'+olt1+'");'
                cursor.execute(sql_door_alarm)
                connection.commit()
                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","BUNKER_OPEN","START","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()
                kirim = " Bunker baterai OLT : "+olt2+" terbuka "
                kirim = str(kirim)
                msg_maingroup = url_maingroup+kirim
                requests.get(msg_maingroup)
                #msg_mtcgroup = url_mtcgroup+kirim
                #requests.get(msg_mtcgroup)
                #msg_patroligroup = url_patroligroup+kirim
                #requests.get(msg_patroligroup)
            
            if "DOOR_ALM" in str(output) and "Current Alarm" in str(output) and "DOOR_OPEN" not in str(mo_door):
                cursor = connection.cursor()
                sql_door_alarm = 'INSERT INTO `olt_warningdoor`(`ip`,`status`,`versi`) VALUES ("'+olt0+'","DOOR_OPEN","'+olt1+'");'
                cursor.execute(sql_door_alarm)
                connection.commit()
                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","DOOR_OPEN","START","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()
                kirim = " Pintu kabinet OLT : "+olt2+" terbuka "
                kirim = str(kirim)
                msg_maingroup = url_maingroup+kirim
                requests.get(msg_maingroup)
                #msg_mtcgroup = url_mtcgroup+kirim
                #requests.get(msg_mtcgroup)
                #msg_patroligroup = url_patroligroup+kirim
                #requests.get(msg_patroligroup)
            
            

            if "DOOR_ALM" not in str(output) and olt0 in str(mo_door) and "DOOR_OPEN" in str(mo_door) and "Current Alarm" in str(output):
                cursor = connection.cursor()
                sql_door_alarm = 'DELETE FROM `olt_warningdoor` WHERE `ip`="'+olt0+'" AND `status`="DOOR_OPEN";'
                cursor.execute(sql_door_alarm)
                connection.commit()
                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","DOOR_CLOSED","END","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()
                kirim = " Pintu kabinet OLT : "+olt2+" tertutup "
                kirim = str(kirim)
                msg_maingroup = url_maingroup+kirim
                requests.get(msg_maingroup)
                '''msg_mtcgroup = url_mtcgroup+kirim
                requests.get(msg_mtcgroup) 
                msg_patroligroup = url_patroligroup+kirim
                requests.get(msg_patroligroup)'''
            
            if "Battery_bunker_door_alarm" not in str(output) and olt0 in str(mo_door) and "BUNKER_OPEN" in str(mo_door) and "Current Alarm" in str(output):
                cursor = connection.cursor()
                sql_door_alarm = 'DELETE FROM `olt_warningdoor` WHERE `ip`="'+olt0+'" AND `status`="BUNKER_OPEN";'
                cursor.execute(sql_door_alarm)
                connection.commit()
                ct = datetime.datetime.now()
                sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","BUNKER_CLOSED","END","'+str(ct)+'");'
                cursor.execute(sql_log)
                connection.commit()
                kirim = " Bunker baterai OLT : "+olt2+" tertutup "
                kirim = str(kirim)
                msg_maingroup = url_maingroup+kirim
                requests.get(msg_maingroup)
                '''msg_mtcgroup = url_mtcgroup+kirim
                requests.get(msg_mtcgroup)
                msg_patroligroup = url_patroligroup+kirim
                requests.get(msg_patroligroup)'''
            
            #if "Battery_bunker_door_alarm" in str(output):
               # cursor = connection.cursor()
                #sql_door_alarm == 'INSERT INTO `olt_warning`(`ip`,`status`,`versi`) VALUES ("'+olt0+'","BatteryBunker_OPEN","'+olt1+'");'
                #cursor.execute(sql_door_alarm)
                #connection.commit()