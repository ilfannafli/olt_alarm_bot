import paramiko
import pymysql
def custom(connection):
    cursor = connection.cursor()
    sql_list = 'select user,pass from data_login;'
    cursor.execute(sql_list)
    data = cursor.fetchone()
    #ip, user, password telnet
    ip_address = "10.60.190.16"
    usr = data[0]
    pwd = data[1]

    return ip_address,usr,pwd


connection = pymysql.connect(host='localhost',user='root',password='',db='testoltkp')
cursor = connection.cursor()

ip_address,usr,pwd = custom(connection)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=ip_address, username=usr, password=pwd)
print("SSH connection is successfully established with ", ip_address)