import re
import paramiko
import time
import requests
import schedule
import pymysql  
import datetime

def percentage(olt_version,shell):

    if olt_version == "AN5516-04": 
        cmd = ["cd device",
                "show hcu env_para card"]
        output = shell.recv(65535)
        match = re.search(r"battery_capacity (\d+\.\d+)", output)
        loadcurrent = float(match.group(1))
        return loadcurrent   
                
    if olt_version == "AN6000-2": 
        cmd = ["config",
                "show hcu card"]
        output = shell.recv(65535)
        match = re.search(r"battery_capacity (\d+\.\d+)", output)
        loadcurrent = float(match.group(1))
        return loadcurrent 