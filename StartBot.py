from subprocess import call
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import sys
import time
import os
print("Menjalankan bot Outdoor")

pid = os.getpid()
with open("pid_bot.txt", "w") as file:
    file.write(str(pid)) 
files=('botOutdoor1.py','botOutdoor2.py','botOutdoor3.py','botOutdoor4.py','botOutdoor5.py','botOutdoor6.py','botOutdoor7.py','botOutdoor8.py','botOutdoor9.py','botOutdoor10.py','botOutdoor11.py','botOutdoor12.py','botOutdoor13.py','botOutdoor14.py','botOutdoor15.py')
#files=('botOutdoor1.py','botOutdoor2.py','botOutdoor3.py')
def thread_function(file):
    while True:
        try:
            time.sleep(1)
            call(["python", file])
        except:
            print("Bot cek OLT outdoor gagal terhubung dengan SSH. Restarting...")
            continue

with ThreadPoolExecutor(max_workers=15) as executor:
    for file in files :
        executor.submit(thread_function, file) 

