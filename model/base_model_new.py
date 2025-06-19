import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from joblib import dump

def base_model(ip):
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv("C:\\xampp\\htdocs\\olt-alarm-bot\\model\\test_dropvoltage.csv")

    # Extract the values for X and y
    X_train = df[['voltage', 'current_load', 'Percentage']].values
    y_train = df['time_elapsed'].values

    # Scale the data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)

    # Create an ElasticNet model with the specified parameters
    pipe = ElasticNet(warm_start=True, tol=0.01, selection='random', random_state=2019, precompute=False, positive=False, max_iter=100000, l1_ratio=0.5771543086172344, fit_intercept=True, copy_X=False, alpha=0.043983174666502235)

    # Fit the model to the training data
    pipe.fit(X_train, y_train)

    # Construct the file path for the corresponding ip
    file_path = "C:\\xampp\\htdocs\\olt-alarm-bot\\model\\{}_model.joblib".format(ip)

    # Create a joblib file for the trained model
    dump(pipe, file_path)

    return