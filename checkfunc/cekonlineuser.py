import paramiko
import time
import requests
import schedule
import pymysql  
import datetime
import re
from checkfunc import sendCommand

def user(input,shell,olt):
    if input == "AN5516-04": 
        sendCommand.wait_for_output(shell, olt, "cd /\n", "#")
        sendCommand.wait_for_output(shell, olt, "cd onu\n", "#")
        outputonline = sendCommand.wait_for_output(shell, olt, "show onu auth-and-online statistics level system\n", "#")
        
        #print(outputonline.decode())
        outputonline=str(outputonline)
        onlinematch = re.search(r"\d+/\d+ ", outputonline)  
    if input == "AN6000-2": 
        outputonline = sendCommand.wait_for_output(shell, olt, "show onu auth-and-online statistics level system\n", "#")
        #print(outputonline.decode())
        outputonline=str(outputonline)
        onlinematch = re.search(r"\d+/\d+ ", outputonline)  

    return onlinematch