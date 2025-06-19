import numpy as np
from joblib import load
import pymysql
import os
from model import base_model
import datetime
from sklearn.preprocessing import StandardScaler

def predict(ip):
    
    # Connect to the MySQL database and retrieve data for the specified IP
    connection = pymysql.connect(host='localhost',user='root',password='',db='testoltkp')
    cursor = connection.cursor()
    sql_list = 'SELECT ip, voltage, current_load, Percentage, capacity, time, time_elapsed FROM test_dropvoltage WHERE ip = "'+ip+'" ORDER BY time DESC LIMIT 1;'
    cursor.execute(sql_list)
    data = cursor.fetchall()

    # Construct the file path for the corresponding IP
    file_path = "C:\\xampp\\htdocs\\olt-alarm-bot\\model\\{}_model.joblib".format(ip)

    # Load a saved model for the corresponding IP    
    pipe = load(file_path)

    # Predict the time elapsed until the battery is dead
    scaler = StandardScaler()
    X_dead = np.array([[45, float(d[2]), 7.5] for d in data])
    X_dead = scaler.transform(X_dead)
    y_dead = pipe.predict(X_dead)

    # Calculate and format the remaining time until the battery is dead 
    y_current = [float(d[6]) for d in data]
    remaining_s = int(y_dead - y_current)

    if remaining_s < 0:
        remaining_string = "(Tidak terkalkulasi)"
        time_of_death_string = "(Tidak tersedia, harap tunggu selama 30 menit)"

    else:
        remaining_string = "{:02d} JAM {:02d} MENIT {:02d} DETIK".format(remaining_s // 3600, (remaining_s % 3600) // 60, remaining_s % 60)

        # Calculate and format the time of death of the battery
        time_of_death = datetime.datetime.now() + datetime.timedelta(seconds=remaining_s)
        time_of_death_string = time_of_death.strftime("%d-%m-%Y %H:%M:%S")

    # Return the remaining time and time of death strings
    return remaining_string, time_of_death_string
