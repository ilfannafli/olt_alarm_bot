import paramiko
import time
import requests
import schedule
import pymysql  
import datetime
import logingood
import loginbad
def cekpos(pos,brand,olt0,olt2,ceklogin,testping,mo_down,connection,url_mtcgroup,url_maingroup,pic) :
#cek OLT INDOOR dan MSAN
        if pos == "INDOOR":
            if brand == "FIBERHOME" or brand == "ALU":
                if "Login" not in str(ceklogin) or "login" not in str(ceklogin) and "bytes" not in str(testping) and olt0 not in str(mo_down):
                    loginbad.bad(olt0,olt2,connection,url_mtcgroup,url_maingroup,pic)

                elif "Login" in str(ceklogin) or "login" not in str(ceklogin) and olt0 in str(mo_down) and "bytes" in str(testping):
                    logingood.good(olt0,connection)

                else:
                    return

            elif brand == "ZTE":
                 if "Username" not in str(ceklogin) and "bytes" not in str(testping) and olt0 not in str(mo_down):
                    loginbad.bad(olt0,olt2,connection,url_mtcgroup,url_maingroup,pic)

                 elif "Username" in str(ceklogin) and olt0 in str(mo_down) and "bytes" in str(testping):
                    logingood.good(olt0,connection)

            else:
                return
        
        elif pos == "MSAN":
            if "bytes" not in str(testping) and olt0 not in str(mo_down):
               loginbad.bad(olt0,olt2,connection,url_mtcgroup,url_maingroup,pic)

            elif olt0 in str(mo_down) and "bytes" in str(testping):
                logingood.good(olt0,connection)

            else:
                return

