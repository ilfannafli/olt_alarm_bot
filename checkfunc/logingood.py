import paramiko
import time
import requests
import schedule
import pymysql  
import datetime            
def good(olt0,connection):
    cursor = connection.cursor()
    sql_delete_table_down = 'DELETE FROM `olt_down` WHERE ip="'+olt0+'";'
    cursor.execute(sql_delete_table_down)
    connection.commit()

    ct = datetime.datetime.now()
    sql_log = 'INSERT INTO `olt_log`(`ip`,`status`,`tag`,`time`) VALUES ("'+olt0+'","OLT DOWN","END","'+str(ct)+'");'
    cursor.execute(sql_log)
    connection.commit()
    return