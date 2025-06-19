def custom(connection):
    #alamat grup Telegram
    url_maingroup = 'https://api.telegram.org/bot8108321673:AAGMkFTivNWOirWfL3qh2pDVao2tLhohadA/sendMessage?chat_id=-4948272871&text='
    url_mtcgroup = 'https://api.telegram.org/bot8108321673:AAGMkFTivNWOirWfL3qh2pDVao2tLhohadA/sendMessage?chat_id=-1001710408993&text='
    url_kpgroup = 'https://api.telegram.org/bot8108321673:AAGMkFTivNWOirWfL3qh2pDVao2tLhohadA/sendMessage?chat_id=-865403076&text='
    url_patroligroup = 'https://api.telegram.org/bot8108321673:AAGMkFTivNWOirWfL3qh2pDVao2tLhohadA/sendMessage?chat_id=-888946770&text='
    
    cursor = connection.cursor()
    sql_list = 'select user,pass from data_login;'
    cursor.execute(sql_list)
    data = cursor.fetchone()
    #ip, user, password telnet
    ip_address = "10.60.190.16"
    usr = data[0]
    pwd = data[1]

    return url_maingroup,url_mtcgroup,url_kpgroup, url_patroligroup, ip_address,usr,pwd