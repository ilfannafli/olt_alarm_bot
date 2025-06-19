def getID(connection,ip):
    cursor = connection.cursor()
    sql_list = 'SELECT id_telegram_group.id_telegram, olt_list.ip FROM olt_list JOIN id_telegram_group  ON olt_list.datel = id_telegram_group.witel WHERE olt_list.ip = "'+ip+'";'
    cursor.execute(sql_list)
    id_group = cursor.fetchone()

    grupWitel = "https://api.telegram.org/bot8108321673:AAGMkFTivNWOirWfL3qh2pDVao2tLhohadA/sendMessage?chat_id=" + id_group[0] + "&text="

    return grupWitel