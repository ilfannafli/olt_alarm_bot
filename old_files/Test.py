import pymysql  
import telebot

connection = pymysql.connect(host='127.0.0.1',user='root',password='',db='tesoltkp')
#cursor = connection.cursor()
#sql_list = 'select ip,status,tag,time from olt_log;'
#cursor.execute(sql_list)
#data = cursor.fetchall()

api = '5933357528:AAGoECge8eGvPFQqG3Y1xfXeA3-yu-tVy8Q'
bot = telebot.TeleBot(api)

@bot.route('/cek')
def pesan(message):

    cursor = connection.cursor()
    sql_list_acvoldown = 'SELECT olt_list.hostname, olt_list.ip FROM olt_list join olt_warning on olt_list.ip=olt_warning.ip WHERE olt_warning.status="ACVOLDOWN";'
    cursor.execute(sql_list_acvoldown)
    data_acvoldown = cursor.fetchall()

    cursor = connection.cursor()
    sql_list_down = 'SELECT olt_list.hostname, olt_list.ip FROM olt_list join olt_down on olt_list.ip=olt_down.ip WHERE olt_down.status="DOWN";'
    cursor.execute(sql_list_down)
    data_down = cursor.fetchall()
    
    pesan_header_av = 'LIST OLT LISTRIK MATI:\n'
    pesan_list_av = ''
    no_av = 0
    for list_av in data_acvoldown :
        no_av += 1        
        pesan_list_av = pesan_list_av+str(no_av)+'. '+list_av[0]+' ('+list_av[1]+') ' + '\n'
    pesan_av = pesan_header_av + pesan_list_av + '\n'

    pesan_header_down = 'LIST OLT DOWN:\n'
    pesan_list_down = ''
    no_dw = 0
    for list_down in data_down :
        no_dw += 1       
        pesan_list_down = pesan_list_down+str(no_dw)+'. '+list_down[0]+' ('+list_down[1]+') ' + '\n'
        
    if no_av == 0 and no_dw == 0: 
            pesan = 'Seluruh OLT UP'
    else:
        pesan_down = pesan_header_down + pesan_list_down + '\n'
        pesan=pesan_av+pesan_down
        
    chat_dest = message['chat']['id']
    bot.send_message(chat_dest, pesan)

if __name__ == '__main__':
    bot.config['api_key'] = '5933357528:AAGoECge8eGvPFQqG3Y1xfXeA3-yu-tVy8Q'
    bot.reply_to('/cek', pesan)
    bot.poll(debug=True)