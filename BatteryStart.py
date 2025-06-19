from subprocess import call
import sys
import time
import os
pid = os.getpid()
with open("pid_bat.txt", "w") as file:
    file.write(str(pid)) 
while True:
    try:
        time.sleep(1)
        call(["python", "BatteryCheckV4.py"])
        print("Running...")
    except:
        print("Error pada cek baterai. Restarting...")
        continue

