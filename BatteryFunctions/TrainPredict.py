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

def TP(olt0,olt3,voltase,bat_percentage,current_load,useronline,url_maingroup,url_mtcgroup,url_kpgroup):
    train.train(olt0)
    remaining, jatuhtempo = predict.predict(olt0)
    info = "Sisa waktu pada OLT "+olt3+" ("+olt0+") adalah: "+remaining+" dengan predikisi mati pada : "+jatuhtempo+" ( Voltase = "+voltase+" | Sisa baterai = "+bat_percentage+" | Beban Arus = " +current_load+" | Online User = "+useronline+" )"
    msg_maingroup = url_maingroup+info
    requests.get(msg_maingroup)
    msg_mtcgroup = url_mtcgroup+info
    requests.get(msg_mtcgroup)
    msg_kpgroup = url_kpgroup+info
    requests.get(msg_kpgroup)
    print("Sisa waktu pada OLT "+olt3+" ("+olt0+") adalah: "+remaining+" jam ,( Voltase = "+voltase+" | Sisa baterai = "+bat_percentage+" | Beban Arus = " +current_load)
    return