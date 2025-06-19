import paramiko
import time
import requests
import schedule
import pymysql  
from datetime import datetime
import re
from model import train,predict
import telebot
import math as mt
from getfunc import getLoginData
import os

def UD(olt0,firsttime0,floorseci,voltase,bat_percentage,current_load,cursor,connection,sisabaterai,waktu,sekarang):
    datetime_object = datetime.strptime(firsttime0, '%Y-%m-%d %H:%M:%S')
    timeelapsed = sekarang - datetime_object
    elapsedsecond = timeelapsed.total_seconds()
    floorseci = mt.floor(elapsedsecond/1800)
    elapsedsecond = str(elapsedsecond)
    sql_insert_table_warning = 'INSERT INTO `test_dropvoltage`(`ip`,`voltage`,`current_load`,`Percentage`,`capacity`,`time`,`time_elapsed`) VALUES ("'+olt0+'","'+voltase+'","'+current_load+'","'+bat_percentage+'","'+sisabaterai+'","'+waktu+'","'+elapsedsecond+'");'
    cursor.execute(sql_insert_table_warning)
    connection.commit()

    return floorseci