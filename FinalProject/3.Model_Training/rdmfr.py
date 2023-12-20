import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
from joblib import dump

df = pd.read_csv("E:\data0199.csv")


X = df.drop('agbd', axis=1)
y = df['agbd']

# Split the data into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Initialize the random forest regression model.
rf_model = RandomForestRegressor(n_estimators=50, random_state=42)

# Train the model.
rf_model.fit(X_train, y_train)

# Make predictions on the test and train set.
predictions = rf_model.predict(X_test)
predictions2 = rf_model.predict(X_train)


# Calculate evluation metrics
rmse = np.sqrt(mean_squared_error(y_test, predictions))
print(f'Test set RMSE: {rmse}')

r2 = r2_score(y_test, predictions)
print(f'Test set r2: {r2}')

mae = mean_absolute_error(y_test, predictions)
print("Test set MAE: ", mae)

me = np.mean(predictions-y_test)
print("Test set ME: ", me)


rmse2 = np.sqrt(mean_squared_error(y_train, predictions2))
print(f'Train set RMSE: {rmse2}')

r22 = r2_score(y_train, predictions2)
print(f'Train set r2: {r22}')

mae2 = mean_absolute_error(y_train, predictions2)
print("Train set MAE: ", mae2)

me2 = np.mean(predictions2-y_train)
print("Train set ME: ", me2)


# Save the model for predictions
dump(rf_model, 'rfmodel.joblib')
