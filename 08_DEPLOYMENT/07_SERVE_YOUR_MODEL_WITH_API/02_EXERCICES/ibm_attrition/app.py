import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List
from fastapi import FastAPI

description = """
This API provide endpoints allowing to build an interactive Dashboard that will help HR know who are their employees and which ones are likely to quit.

## EDA

* `/preview` To be able to preview a few rows of the dataset
* `/unique-values` To be able to get unique values of a given column in the dataset

## Data operations

* `/groupby` To be able to group by a given column and chose an aggregation metric
* `/filterby` To be able to filter by one or several, categories within your dataset
* `/quantile` To be able to retrieve the top x% or bottom x% values of a given column in the dataset

Check out documentation below 👇 for more information on each endpoint.
"""

tags_metadata = [
    {
        "name": "EDA",
        "description": "Endpoints allowing to make basic Exploratory Data Analysis (EDA)"
    },
    {
        "name": "Data operations",
        "description": "Endpoints allowing to make operations on Data (groupBy, filterBy, quantile)"
    }   
]

app = FastAPI(
    title="IBM employees API ",
    description=description,
    version="0.1",
    contact={
        "name": "Backend Team",
        "url": "https://backend-team.ibm",
    },
    openapi_tags=tags_metadata
)

class GroupBy(BaseModel):
    column: str
    aggregation_metric: Literal["sum", "mean", "max", "min", "median", "count"]

class FilterBy(BaseModel):
    column: str
    category: List[str]


@app.get("/preview", tags=["EDA"])
async def preview_employees(rows: int=5):
    """
    Get a dataset preview.
    
    * `rows` : The number of rows you want to preview (default value `5`)
    """

    dataset = pd.read_excel("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/ibm_hr_attrition.xlsx")

    return dataset.head(rows).to_json()


@app.get("/unique-values", tags=["EDA"])
async def unique_values(column: str):
    """
    Get unique values from a column.

    * `column` : The column you want to retrieve unique values from
    """

    dataset = pd.read_excel("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/ibm_hr_attrition.xlsx")
    
    return pd.Series(dataset[column].unique()).to_json()


@app.post("/group_by", tags=["Data operations"])
async def group_by(group_by: GroupBy):
    """
    Get a dataset grouped by one or several columns.

    * `column` : The column you want to grouped by
    * `aggregation_metric` : Aggregation metric to grouped by, within `sum`, `mean`, `max`, `min`, `median`, `count`
    """
    
    dataset = pd.read_excel("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/ibm_hr_attrition.xlsx")

    aggregation_function = getattr(pd.core.groupby.generic.DataFrameGroupBy, group_by.aggregation_metric)

    return aggregation_function(dataset.groupby(group_by.column)).to_json()


@app.post("/filter_by", tags=["Data operations"])
async def filter_by(filter_by: FilterBy):
    """
    Get a dataset filtered by one or several categories on one column.
    
    * `column` : The column you want to filtered by
    * `category` : Categories (at least one) to filtered by, within possible value for the column
    """

    dataset = pd.read_excel("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/ibm_hr_attrition.xlsx")

    return dataset[dataset[filter_by.column].isin(filter_by.category)].to_json()

@app.get("/quantile", tags=["Data operations"])
async def quantile(column: str , percentage: float, top: bool = True):
    """
    Get a dataset filtered by top or lowest quantile on a column.

    * `column` : The column you want to filtered by
    * `percentage` : The quartile percentage
    * `top` : The top or lowest quantile (default value `True`)
    """

    dataset = pd.read_excel("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/ibm_hr_attrition.xlsx")

    if percentage <= 0.0 or percentage >= 1.0 :
        return "Percentage must be between 0.0 and 1.0 (excluded)"
    
    if top :
        dataset = dataset[dataset[column] > dataset[column].quantile(1-percentage)]
    else :
        dataset = dataset[dataset[column] < dataset[column].quantile(percentage)]

    return dataset.to_json()