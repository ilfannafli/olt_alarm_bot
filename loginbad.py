import paramiko
import time
import requests
import schedule
import pymysql  
import datetime
import CheckOLTVersion as OLTVer

def bad(olt0,olt2,connection,url_mtcgroup,url_maingroup,pic):
    cursor = connection.cursor()
    sql_insert_table_warning = 'INSERT INTO `olt_down`(`ip`,`status`) VALUES ("'+olt0+'","DOWN");'
    cursor.execute(sql_insert_table_warning)
    connection.commit()

    ct = datetime.datetime.now()
    sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","OLT DOWN","START","'+str(ct)+'");'
    cursor.execute(sql_log)
    connection.commit()           

    msg_maingroup = url_maingroup+olt2+' ('+olt0+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'+pic
    requests.get(msg_maingroup)
    msg_mtcgroup = url_mtcgroup+olt2+' ('+olt0+') tidak dapat diremote.\nMini OLT terindikasi LOS\n'+pic
    requests.get(msg_mtcgroup)   
    return