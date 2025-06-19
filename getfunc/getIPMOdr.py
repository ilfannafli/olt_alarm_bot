import paramiko
import time
import requests
import schedule
import pymysql  
import datetime

def IPMOdr(olt0,connection):      
        cursor = connection.cursor()
        sql_warning = 'select ip,status from olt_warningdoor where ip="'+olt0+'";'
        cursor.execute(sql_warning)
        mo_door = cursor.fetchall()
        return mo_door