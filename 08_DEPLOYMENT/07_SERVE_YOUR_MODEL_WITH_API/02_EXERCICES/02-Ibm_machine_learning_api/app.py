import mlflow 
import uvicorn
import json
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile

description = """
Human Resources API helps you learn more about you're companies employee. 
The goal of this api is to serve data that help managers understand how the company is organized and make better decisions to 
keep the top talents. 

## Preview

Where you can: 
* `/preview` a few rows of your dataset
* get `/unique-values` of a given column in your dataset

## Categorical

Where you can: 
* `/groupby` a given column and chose an aggregation metric 
* `/filter-by` one of several categories within your dataset 

## Numerical 

Where you can: 
* Get a subset of your data given a certain `/quantile` 


## Machine-Learning 

Where you can:
* `/predict` if one person is likely to quit the company
* `/batch-predict` where you can upload a file to get predictions for several employees


Check out documentation for more information on each endpoint. 
"""

tags_metadata = [
    {
        "name": "Categorical",
        "description": "Endpoints that deal with categorical data",
    },

    {
        "name": "Numerical",
        "description": "Endpoints that deal with numerical data"
    },

    {
        "name": "Preview",
        "description": "Endpoints that quickly explore dataset"
    },

    {
        "name": "Predictions",
        "description": "Endpoints that uses our Machine Learning model for detecting attrition"
    }
]

app = FastAPI(
    title="👨‍💼 HR API",
    description=description,
    version="0.1",
    contact={
        "name": "HR API - by Jedha",
        "url": "https://jedha.co",
    },
    openapi_tags=tags_metadata
)

class GroupBy(BaseModel):
    column: str
    by_method: Literal["mean", "median", "max", "min", "sum", "count"] = "mean"

class FilterBy(BaseModel):
    column: str
    by_category: List[str]= None

class PredictionFeatures(BaseModel):
    Age: Union[int, float]
    BusinessTravel: str
    DailyRate: Union[int, float]
    Department: str
    DistanceFromHome: Union[int, float]
    Education: Union[int, float]
    EducationField: str
    EmployeeCount: Union[int, float]
    EmployeeNumber: Union[int, float]
    EnvironmentSatisfaction: Union[int, float]
    Gender: str
    HourlyRate: Union[int, float]
    JobInvolvement: Union[int, float]
    JobLevel: Union[int, float]
    JobRole: str
    JobSatisfaction: Union[int, float]
    MaritalStatus: str
    MonthlyIncome: Union[int, float]
    MonthlyRate: Union[int, float]
    NumCompaniesWorked: Union[int, float]
    Over18: str
    OverTime: str
    PercentSalaryHike: Union[int, float]
    PerformanceRating: Union[int, float]
    RelationshipSatisfaction: Union[int, float]
    StandardHours: Union[int, float]
    StockOptionLevel: Union[int, float]
    TotalWorkingYears: Union[int, float]
    TrainingTimesLastYear: Union[int, float]
    WorkLifeBalance: Union[int, float]
    YearsAtCompany: Union[int, float]
    YearsInCurrentRole: Union[int, float]
    YearsSinceLastPromotion: Union[int, float]
    YearsWithCurrManager: Union[int, float]

@app.get("/preview", tags=["Preview"])
async def random_employees(rows: int=10):
    """
    Get a sample of your whole dataset. 
    You can specify how many rows you want by specifying a value for `rows`, default is `10`
    """
    df = pd.read_excel("data/ibm_hr_attrition.xlsx")
    sample = df.sample(rows)
    return sample.to_json()


@app.get("/unique-values", tags=["Preview"])
async def unique_values(column: str):
    """
    Get unique values from a given column 
    """
    df = pd.read_excel("data/ibm_hr_attrition.xlsx")
    df = pd.Series(df[column].unique())

    return df.to_json()

@app.get("/quantile", tags=["Numerical"])
async def quantile(column: str , percent: float = 0.1, top: bool = True):
    """
    Get a values of HR dataset according above or below a given quantile. 
    *i.e* with this dataset, you can have the top 10% values of the dataset given a certain column
    
    You can choose whether you want the top quantile or the bottom quantile by specify `top=True` or `top=False`. Default value is `top=True`
    Accepted values for percentage is a float between `0.01` and `0.99`, default is `0.1`
    """

    df = pd.read_excel("data/ibm_hr_attrition.xlsx")

    if percent > 0.99 or percent <0.01:
        msg = "percentage value is not accepted"
        return msg
    else:
        if top:
            df = df[ df[column] > df[column].quantile(1-percent)]
        else:
            df = df[ df[column] < df[column].quantile(percent)]

        return df.to_json()

@app.post("/groupby", tags=["Categorical"])
async def group_by(groupBy: GroupBy):
    """
    Get data grouped by a given column. Accepted columns are:

    * `["Attrition","BusinessTravel", "Department", "EducationField", "Gender", "JobRole", "MaritalStatus", "Over18", "OverTime"]`

    You can use different method to group by category which are:

    * `mean`
    * `median`
    * `min`
    * `max`
    * `sum`
    * `count`
    """
    
    df = pd.read_excel("data/ibm_hr_attrition.xlsx")

    method = groupBy.by_method

    if method=="mean":
        df = df.groupby(groupBy.column).mean()
    if method=="median":
        df = df.groupby(groupBy.column).median()
    if method=="min":
        df = df.groupby(groupBy.column).min()
    if method=="max":
        df = df.groupby(groupBy.column).max()
    if method=="sum":
        df = df.groupby(groupBy.column).sum()
    if method=="count":
        df = df.groupby(groupBy.column).count()

    return df.to_json()

@app.post("/filter-by", tags=["Categorical"])
async def filter_by(filterBy: FilterBy):
    """
    Filter by one or more categories in a given column. Columns possible values are:

    * `["Attrition","BusinessTravel", "Department", "EducationField", "Gender", "JobRole", "MaritalStatus", "Over18", "OverTime"]`

    Check values within dataset to know what kind of `categories` you can filter by. You can use `/unique-values` path to check them out.
    `categories` must be `list` format.
    """

    df = pd.read_excel("data/ibm_hr_attrition.xlsx")

    if filterBy.by_category != None:
        df = df[df[filterBy.column].isin(filterBy.by_category)]
        return df.to_json()
    else:
        msg = "Please chose a column to filter by"
        return msg


@app.post("/predict", tags=["Machine-Learning"])
async def predict(predictionFeatures: PredictionFeatures):
    """
    Prediction for one observation. Endpoint will return a dictionnary like this:

    ```
    {'prediction': PREDICTION_VALUE[0,1]}
    ```

    You need to give this endpoint all columns values as dictionnary, or form data.
    """
    # Read data 
    df = pd.DataFrame(dict(predictionFeatures), index=[0])

    # Log model from mlflow 
    logged_model = 'runs:/1454214014ee4a14942fbfede6fd5e3e/ibm_attrition_detector'

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    prediction = loaded_model.predict(df)

    # Format response
    response = {"prediction": prediction.tolist()[0]}
    return response


@app.post("/batch-predict", tags=["Machine-Learning"])
async def batch_predict(file: UploadFile = File(...)):
    """
    Make prediction on a batch of observation. This endpoint accepts only **csv files** containing 
    all the trained columns WITHOUT the target variable. 
    """
    # Read file 
    df = pd.read_csv(file.file)

    # Log model from mlflow 
    logged_model = 'runs:/1454214014ee4a14942fbfede6fd5e3e/ibm_attrition_detector'

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    predictions = loaded_model.predict(df)

    return predictions.tolist()