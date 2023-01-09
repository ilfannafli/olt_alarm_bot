def IPMO(olt0):      
        cursor = connection.cursor()
        sql_warning = 'select ip,status from olt_warning where ip="'+olt0+'";'
        cursor.execute(sql_warning)
        mo_warning = cursor.fetchall()
        return