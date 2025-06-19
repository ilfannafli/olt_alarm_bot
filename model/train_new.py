from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import RandomizedSearchCV
from joblib import dump, load
import pymysql
import os
import numpy as np

def train(ip):
    
    # Read from sql db
    connection = pymysql.connect(host='localhost',user='root',password='',db='testoltkp')
    cursor = connection.cursor()
    sql_list = 'SELECT ip, voltage, current_load, Percentage, capacity, time, time_elapsed FROM test_dropvoltage WHERE ip = "'+ip+'";'
    cursor.execute(sql_list)
    data = cursor.fetchall()
    
    # Construct the file path for the corresponding ip
    file_path = "C:\\xampp\\htdocs\\olt-alarm-bot\\model\\{}_model.joblib".format(ip)

    # Checking if path exist
    if os.path.isfile(file_path):
    # Load a saved model for the given ip
        pipe = load(file_path)
    else:
        # Use master
        pipe = load("C:\\xampp\\htdocs\\alarm_olt\\olt-alarm-bot\\model\\master_model.joblib")

    # Extract the input features X and the output label y
    X_train = [ [float(d[1]), float(d[2]), float(d[3]) ] for d in data ]
    y_train = [ d[6] for d in data ]

    # Scale the data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)

    # Define the parameter grid to search
    param_grid = {
            'alpha': np.logspace(-5, 1, 100),
            'l1_ratio': np.linspace(0, 1, 100),
            'warm_start': [True, False],
            'selection': ['random']
        }

    # Create the randomized search object
    random_search = RandomizedSearchCV(pipe, param_grid, cv=5, n_iter=10000, n_jobs=-1, verbose=0, scoring='neg_mean_squared_error')

    # Fit the randomized search object to the data
    random_search.fit(X_train, y_train)

    # Update the model with the best hyperparameters
    best_params = random_search.best_params_
    pipe.set_params(**best_params)
    pipe.fit(X_train, y_train)

    # Save the updated model 
    dump(pipe, file_path)

    return