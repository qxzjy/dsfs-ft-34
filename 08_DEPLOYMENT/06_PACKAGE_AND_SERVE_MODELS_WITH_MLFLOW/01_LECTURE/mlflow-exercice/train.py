import argparse
import pandas as pd
import time
import mlflow
from mlflow.models.signature import infer_signature
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import  StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline


if __name__ == "__main__":

    print("training model...")
    
    # Time execution
    start_time = time.time()

    # Call mlflow autolog
    mlflow.sklearn.autolog() 

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_estimators", default=1)
    parser.add_argument("--min_samples_split", default=2)
    args = parser.parse_args()

    with mlflow.start_run() as run:

        # Import dataset
        df = pd.read_csv("https://julie-2-next-resources.s3.eu-west-3.amazonaws.com/full-stack-full-time/linear-regression-ft/californian-housing-market-ft/california_housing_market.csv")

        # X, y split 
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

        # Train / test split 
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

        # Pipeline 
        n_estimators = int(args.n_estimators)
        min_samples_split=int(args.min_samples_split)

        model = Pipeline(steps=[
            ("standard_scaler", StandardScaler()),
            ("Regressor",RandomForestRegressor(n_estimators=n_estimators, min_samples_split=min_samples_split))
        ])

        # Log experiment to MLFlow

        #with mlflow.start_run(experiment_id = experiment.experiment_id):
        model.fit(X_train, y_train)
        predictions = model.predict(X_train)
        
    print("...Done!")
    print(f"---Total training time: {time.time()-start_time}")