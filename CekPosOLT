import paramiko
import time
import requests
import schedule
import pymysql  
import datetime
import CheckOLTVersion as OLTVer
import logingood
import loginbad

#cek OLT INDOOR dan MSAN
        if olt[3] == "INDOOR" and olt[4] == "FIBERHOME":
            if "Login" not in str(ceklogin) and "bytes" not in str(testping) and olt[0] not in str(mo_down):
              loginbad.bad(olt[0],olt[2])

            elif "Login" in str(ceklogin) and olt[0] in str(mo_down) and "bytes" in str(testping):
                logingood.good(olt[0])

            else:
                return

        elif olt[3] == "INDOOR" and olt[4] == "ZTE":
            if "Username" not in str(ceklogin) and "bytes" not in str(testping) and olt[0] not in str(mo_down):
                loginbad.bad(olt[0],olt[2])

            elif "Username" in str(ceklogin) and olt[0] in str(mo_down) and "bytes" in str(testping):
               logingood.good(olt[0])

            else:
                continue

        elif olt[3] == "INDOOR" and olt[4] == "ALU":
            if "login" not in str(ceklogin) and "bytes" not in str(testping) and olt[0] not in str(mo_down):
               loginbad.bad(olt[0],olt[2])

            elif "login" in str(ceklogin) and olt[0] in str(mo_down) and "bytes" in str(testping):
                logingood.good(olt[0])

            else:
                return