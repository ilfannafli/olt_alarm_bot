from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from joblib import dump, load
import pymysql
import os
from model import base_model

def train(ip):
    
    # Read from sql db
    connection = pymysql.connect(host='localhost',user='root',password='',db='testoltkp')
    cursor = connection.cursor()
    sql_list = 'SELECT ip, voltage, current_load, Percentage, capacity, time, time_elapsed FROM test_dropvoltage WHERE ip = "'+ip+'";'
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

    # Extract the values for input X, output Y
    X = [ [float(d[1]), float(d[2]), float(d[3]) ] for d in data ]
    y = [ d[6] for d in data ]
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Fit the model to the training data
    pipe.fit(X_train, y_train)

    # Use the model to make predictions on the test data
    y_pred = pipe.predict(X_test)

    # Updating the model with the 
    dump(pipe, file_path)

    return