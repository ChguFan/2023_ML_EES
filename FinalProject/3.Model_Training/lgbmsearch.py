import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from lightgbm import LGBMRegressor
from bayes_opt import BayesianOptimization

# Load data
df = pd.read_csv("E:\data0199.csv")
X = df.drop('agbd', axis=1)
y = df['agbd']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the scoring function for LightGBM
def lgbm_eval(n_estimators,max_depth, num_leaves, min_child_samples, colsample_bytree, subsample, learning_rate):
    params = {
        'n_estimators': int(n_estimators),
        'max_depth': int(max_depth),
        'num_leaves': int(num_leaves),
        'min_child_samples': int(min_child_samples),
        'colsample_bytree': colsample_bytree,
        'objective': 'quantile',
        'alpha': 0.5,
        'subsample': subsample,
        'boosting_type': 'gbdt',
        'learning_rate': learning_rate

    }
    lgbm = LGBMRegressor(**params)
    lgbm.fit(X_train, y_train, eval_set=[(X_test, y_test)])
    y_pred = lgbm.predict(X_test)
    return -mean_squared_error(y_test, y_pred)


# Set the range of hyperparameters.
pbounds = {
    'n_estimators': (50, 2000),
    'max_depth': (100, 1000),
    'num_leaves': (1000, 10000),
    'min_child_samples': (10, 200),
    'colsample_bytree': (0.5, 1),
    'subsample': (0.5, 1),
    'learning_rate': (0.01, 0.5)
}

# Optimize hyperparameters using Bayesian Optimization.
optimizer = BayesianOptimization(f=lgbm_eval, pbounds=pbounds, random_state=42)
optimizer.maximize(init_points=50, n_iter=100)

# Output the best parameters.
print("Best parameters：", optimizer.max['params'])
