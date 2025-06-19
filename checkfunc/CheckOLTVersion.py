import paramiko
import time
import requests
import schedule
import pymysql  
import datetime
from checkfunc import sendCommand

def CheckOLTVersion(input,shell,olt):
  if input == "AN5516-04": 
    sendCommand.wait_for_output(shell, olt, "cd service\n", "#")
    sendCommand.wait_for_output(shell, olt, "terminal length 0\n", "#")
    sendCommand.wait_for_output(shell, olt, "cd .\n", "#")
    sendCommand.wait_for_output(shell, olt, "cd maintenance\n", "#")
    sendCommand.wait_for_output(shell, olt, "cd alarm\n", "#")
    output = sendCommand.wait_for_output(shell, olt, "show alarm current\n", "#")
        
    return output                 

    #command list untuk OLT versi AN6000-2           
  if input == "AN6000-2": 
  
    sendCommand.wait_for_output(shell, olt, "config\n", "#")
    sendCommand.wait_for_output(shell, olt, "terminal length 0\n", "#")
    output = sendCommand.wait_for_output(shell, olt, "show alarm current\n", "#")
      
    return output