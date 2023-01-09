import paramiko
import time
import requests
import schedule
import pymysql  
import datetime

def PIC(olt0):        
        cursor = connection.cursor()
        sql_pic = 'SELECT pic.username FROM `pic` JOIN olt_list ON pic.sto=olt_list.sto WHERE olt_list.ip="'+olt0+'";'
        cursor.execute(sql_pic)
        username = cursor.fetchall()
        for pic_id in username:
            pic=str(pic_id[0])
        return pic