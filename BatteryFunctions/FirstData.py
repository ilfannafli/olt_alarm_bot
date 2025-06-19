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

def fd(olt0,olt3,voltase,bat_percentage,current_load,useronline,url_maingroup,url_mtcgroup,url_kpgroup,cursor,connection,sisabaterai,waktu): 
    elapsedsecond=0
    elapsedsecond=str(elapsedsecond)
    sql_insert_table_warning = 'INSERT INTO `test_dropvoltage`(`ip`,`voltage`,`current_load`,`Percentage`,`capacity`,`time`,`time_elapsed`) VALUES ("'+olt0+'","'+voltase+'","'+current_load+'","'+bat_percentage+'","'+sisabaterai+'","'+waktu+'","'+elapsedsecond+'");'
    cursor.execute(sql_insert_table_warning)
    connection.commit()
    firstingfo="STATUS "+olt3+" : VOLTASE = " + voltase + " | ARUS BEBAN = " +current_load+" | ONLINE USER = "+useronline
    msg_maingroup = url_maingroup+firstingfo
    requests.get(msg_maingroup)
    msg_mtcgroup = url_mtcgroup+firstingfo
    requests.get(msg_mtcgroup)
    msg_kpgroup = url_kpgroup+firstingfo
    requests.get(msg_kpgroup)

    return