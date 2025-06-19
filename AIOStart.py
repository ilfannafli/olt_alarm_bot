#import subprocess
from subprocess import call
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import sys
import time
import os
import threading
global pid
import signal

#with open("pid.txt", "r") as file:
    #pid = int(file.read().strip())
pid = os.getpid()    
with open("pid.txt", "w") as file:
    file.write(str(pid))    
#print(pid)                   
files=('StartBot.py','BatteryStart.py')
def thread_function(file, flag):
    process = call(["python", file])
    while not flag.is_set():
        time.sleep(1)
    process.terminate()
    print("Thread terminated:", file)
    os._exit(0)
    print("Process killed:", file)
    
        
def killer(pid, flag):
    while pid !=0:
        #with open("pid.txt", "r") as file:
            #pid = int(file.read().strip())
        #print("masukpid = ",pid)
        time.sleep(1)    
        if pid == 0:
            flag.set()
            print("cya")
            os._exit(0)
if __name__ == '__main__':
    flag = threading.Event()
    with ThreadPoolExecutor(max_workers=3) as executor:
        for file in files :
            executor.submit(thread_function, file, flag)
        executor.submit(killer, pid, flag)