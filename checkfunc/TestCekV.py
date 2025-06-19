import paramiko
import time
import requests
import schedule
import pymysql  
import datetime

def cekvol(olt0,bat_percentage,voltase,current_load,connection) :
                sisabaterai=bat_percentage*40
                cursor = connection.cursor()
                sql_insert_table_warning = 'INSERT INTO `test_dropvoltage`(`ip`,`voltage`,`current_load`,`Percentage`,`capacity`) VALUES ("'+olt0+'","'+voltase+'","'+current_load+'","'+bat_percentage+'","'+sisabaterai+'");'
                cursor.execute(sql_insert_table_warning)
                connection.commit() 