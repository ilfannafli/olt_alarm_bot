import paramiko
import time
import requests
import schedule
import pymysql  
import datetime

def voltase(olt0,connection) :
        voltage=0
        cursor = connection.cursor()
        sql_voltase = 'SELECT olt_gcu.voltase_2jam FROM `olt_gcu` JOIN olt_list ON olt_gcu.ip=olt_list.ip WHERE olt_list.ip="'+olt0+'";'
        cursor.execute(sql_voltase)
        voltase2jam = cursor.fetchall()
        for vol in voltase2jam:
            voltage=str(vol[0])
            
        return voltage