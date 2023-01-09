import paramiko
import time
import requests
import schedule
import pymysql  
import datetime

def mo_down(olt0,connection):      
        cursor = connection.cursor()
        sql_down = 'select ip from olt_down where ip="'+olt0+'";'
        cursor.execute(sql_down)
        mo_down = cursor.fetchall()
        return mo_down