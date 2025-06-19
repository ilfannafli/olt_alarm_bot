import paramiko
import time
import requests
import schedule
import pymysql  
import datetime
from checkfunc import logingood
from checkfunc import loginbad
def cekpos(pos,brand,olt0,olt2,ceklogin,testping,mo_down,connection,url_mtcgroup,url_maingroup) :
#cek OLT INDOOR dan MSAN
        if pos == "INDOOR":
            if brand == "FIBERHOME" or brand == "ALU":
                if "login" not in str(ceklogin).lower() and "bytes" not in str(testping) and olt0 not in str(mo_down):
                    loginbad.bad(olt0,olt2,connection,url_mtcgroup,url_maingroup)

                elif "login" in str(ceklogin).lower() and olt0 in str(mo_down) and "bytes" in str(testping):
                    logingood.good(olt0,connection)

                else:
                     return
            elif brand == "ZTE":
                 if "Username" not in str(ceklogin) and "bytes" not in str(testping) and olt0 not in str(mo_down):
                    loginbad.bad(olt0,olt2,connection,url_mtcgroup,url_maingroup)
                 elif "Username" in str(ceklogin) and olt0 in str(mo_down) and "bytes" in str(testping):
                    logingood.good(olt0,connection)
                 else:
                     return