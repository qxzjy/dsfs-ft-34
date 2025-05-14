import pandas as pd
import mlflow
import time
from sklearn.model_selection import train_test_split, GridSearchCV 
from sklearn.preprocessing import  StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline


if __name__ == "__main__":

    ### NECESSARY SETUP
    #experiment_name="hyperparameter_tuning"
    #mlflow.set_experiment(experiment_name)
    
    print("training model...")
    
    # Time execution
    start_time = time.time()

    # Call mlflow autolog
    mlflow.sklearn.autolog()

    # Import dataset
    df = pd.read_csv("https://julie-2-next-resources.s3.eu-west-3.amazonaws.com/full-stack-full-time/linear-regression-ft/californian-housing-market-ft/california_housing_market.csv")

    # X, y split 
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    # Train / test split 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

    with mlflow.start_run() as run:
        # Pipeline 
        pipe = Pipeline(steps=[
            ("standard_scaler", StandardScaler()),
            ("Random_Forest",RandomForestRegressor())
        ])

        params_grid = {
            "Random_Forest__n_estimators": [10,50,100],
            "Random_Forest__max_depth": [3,10, None]
                    }

        model = GridSearchCV(pipe, params_grid, cv=3, verbose=3)
        model.fit(X_train, y_train)
    
    print("...Training Done!")
    print(f"---Total training time: {time.time()-start_time} seconds")