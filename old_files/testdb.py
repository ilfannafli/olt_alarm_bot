   
import pymysql
 
connection = pymysql.connect(host='127.0.0.1',user='root',password='',db='tesoltkp')
cursor = connection.cursor()
sql_list_acvoldown = 'SELECT olt_list.hostname, olt_list.ip FROM olt_list join olt_warning on olt_list.ip=olt_warning.ip WHERE olt_warning.status="ACVOLDOWN";'
cursor.execute(sql_list_acvoldown)
data_acvoldown = cursor.fetchall()

pesan_list_av=''
no_av=0

for list_av in data_acvoldown :
    cursor=connection.cursor()
    data_bat = 'SELECT voltage, current_load, Percentage FROM test_dropvoltage WHERE ip = %s ORDER BY ip DESC LIMIT 1;'
    cursor.execute(data_bat, (list_av[1],))
    data_baterai = cursor.fetchone()
    no_av += 1        
    print(data_baterai)
    print(data_baterai[0])
    print(data_baterai[1])
    print(data_baterai[2])
    pesan_list_av = pesan_list_av+str(no_av)+'. '+list_av[0]+' ('+list_av[1]+') ' + '\n ( Voltase = '+str(data_baterai[0])+' | Beban Arus = ' + str(data_baterai[1]) + ' | Sisa Baterai = ' + str(data_baterai[2]) + ' )'+ '\n'

pesan_av = pesan_list_av + '\n'

print(pesan_av)