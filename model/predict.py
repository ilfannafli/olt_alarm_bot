import numpy as np
from joblib import load
import pymysql
import os
from model import base_model
import datetime

def predict(ip):

    # Read from sql db
    connection = pymysql.connect(host='localhost',user='root',password='',db='testoltkp')
    cursor = connection.cursor()
    sql_list = 'SELECT ip, voltage, current_load, Percentage, capacity, time, time_elapsed FROM test_dropvoltage WHERE ip = "'+ip+'" ORDER BY time DESC LIMIT 1;'
    cursor.execute(sql_list)
    data = cursor.fetchall()

    # Construct the file path for the corresponding ip
    file_path = "C:\\xampp\\htdocs\\olt-alarm-bot\\model\\{}_model.joblib".format(ip)

    # Checkign if path exist
    if os.path.isfile(file_path):
    # Load a saved model for the given ip
        pipe = load(file_path)
    else:
        # Create one
        base_model.base_model(ip)
        pipe = load(file_path)

    # Predicting the time elapsed until the battery is dead
    X_dead= np.array([[45, float(d[2]), 7.5] for d in data])
    y_dead = pipe.predict(X_dead)

    # Calculating the remaining time until the battery is dead
    y_pred = [float(d[6]) for d in data]

    remaining_s = int(y_dead - y_pred)
    remaining_string = "{:02d} JAM {:02d} MENIT {:02d} DETIK".format(remaining_s // 3600, (remaining_s % 3600) // 60, remaining_s % 60)

    time_of_death = datetime.datetime.now() + datetime.timedelta(seconds=remaining_s)
    time_of_death_string = time_of_death.strftime("%d-%m-%Y %H:%M:%S")

    return remaining_string, time_of_death_string