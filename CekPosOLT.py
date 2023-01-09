import paramiko
import time
import requests
import schedule
import pymysql  
import datetime
import CheckOLTVersion as OLTVer
import logingood
import loginbad
def cekpos(pos,brand,olt0,olt2)
#cek OLT INDOOR dan MSAN
        if pos == "INDOOR":
            if brand == "FIBERHOME" or brand == "ALU":
                if "Login" not in str(ceklogin) or "login" not in str(ceklogin) and "bytes" not in str(testping) and olt[0] not in str(mo_down):
                    loginbad.bad(olt[0],olt[2])

                elif "Login" in str(ceklogin) or "login" not in str(ceklogin) and olt[0] in str(mo_down) and "bytes" in str(testping):
                    logingood.good(olt[0])

                else:
                    return

            elif brand == "ZTE":
                 if "Username" not in str(ceklogin) and "bytes" not in str(testping) and olt[0] not in str(mo_down):
                    loginbad.bad(olt[0],olt[2])

                elif "Username" in str(ceklogin) and olt[0] in str(mo_down) and "bytes" in str(testping):
                    logingood.good(olt[0])

            else:
                continue
        
        elif pos == "MSAN":
            if "bytes" not in str(testping) and olt[0] not in str(mo_down):
               loginbad.bad(olt[0],olt[2])

            elif olt[0] in str(mo_down) and "bytes" in str(testping):
                logingood.good(olt[0])

            else:
                return

