import os
import signal
'''with open("pid.txt", "r") as file:
    pid = int(file.read().strip())
    print(pid)'''
    
try:
    os.kill(8808, signal.SIGTERM)
except OSError as e:
    print("Failed to terminate process:", e)