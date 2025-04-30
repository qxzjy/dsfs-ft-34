import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn import datasets
from sklearn.metrics import r2_score

print("Loading data ...")

dataset = datasets.fetch_california_housing(data_home=None, download_if_missing=True, return_X_y=False)

data = pd.DataFrame(columns=dataset["feature_names"], data=dataset["data"])
data.loc[:,'Price'] = dataset["target"]
data.head()

print("... Done")
print()

print("Data overview :")
print(data.head())
print()

features_list = ["MedInc"]
target_variable = "Price"

X = data.loc[:,features_list]
y = data.loc[:,target_variable]

print("Feature :")
print(X.head())
print()


print("Target :")
print(y.head())
print()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

print("Scaling ...")

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("... Done")
print()

print("Model training ...")

lr = LinearRegression()
lr.fit(X_train, y_train)

print("... Done")
print()

print("Predictions ...")

y_train_pred = lr.predict(X_train)

y_test_pred = lr.predict(X_test)

print("... Done")
print()

print("R2 score on training set : ", r2_score(y_train, y_train_pred))
print("R2 score on test set : ", r2_score(y_test, y_test_pred))