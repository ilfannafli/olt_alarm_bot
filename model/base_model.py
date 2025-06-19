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
    X = df[['voltage', 'current_load', 'Percentage']].values
    y = df['time_elapsed'].values

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Create a pipeline with a StandardScaler and an RFR
    pipe = ElasticNet(alpha=0.0005336699231206312, l1_ratio=0.20202020202020204)

    # Fit the model to the training data
    pipe.fit(X_train, y_train)

    # Use the model to make predictions on the test data
    y_pred = pipe.predict(X_test)

    # Calculate the mean squared error (MSE)
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error: ", mse)

    # Construct the file path for the corresponding ip
    file_path = "C:\\xampp\\htdocs\\olt-alarm-bot\\model\\{}_model.joblib".format(ip)

    # Create a joblib file for the trained model
    dump(pipe, file_path)