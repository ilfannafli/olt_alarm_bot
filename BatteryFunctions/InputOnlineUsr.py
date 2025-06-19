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

def IOU(onlinematch,onlinecheck,olt0,olt3,cursor,connection):    
    if onlinematch:
        if onlinecheck is None :
            useronline = onlinematch.group(0)
            useronline = str(useronline)
            tableonline= 'INSERT INTO `olt_onlineuser`(`ip`, `hostname`, `online`) VALUES ("'+olt0+'","'+olt3+'","'+useronline+'");'
            cursor.execute(tableonline)
            connection.commit()   
        useronline = onlinematch.group(0)
        useronline = str(useronline)
        tableonline= 'UPDATE `olt_onlineuser` SET `online`="'+useronline+'" WHERE `ip`="'+olt0+'";'
        cursor.execute(tableonline)
        connection.commit()
    return useronline 