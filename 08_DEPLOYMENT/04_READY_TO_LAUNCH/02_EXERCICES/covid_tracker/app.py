import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np

### Config
st.set_page_config(
    page_title="Covid Tracker",
    layout="wide"
)

DATA_URL = ('https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv')

### App
st.title("Covid tracker 🦠📊")

st.markdown("""
    With this dashboard, you can follow each covid wave throughout the month of 2021, in EU.
            
    Data from the [European Centre for Disease Prevention and Control (ECDC)](https://www.ecdc.europa.eu/en/publications-data/data-daily-new-cases-covid-19-eueea-country)
""")

st.markdown("---")

# Use `st.cache` when loading data is extremly useful
# because it will cache your data so that your app 
# won't have to reload it each time you refresh your app
@st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL)
    data = data[(data["year"]==2021) & (data["cases"]>0)]
    data["dateRep"] = pd.to_datetime(data["dateRep"], format="%d/%m/%Y")
    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("") # change text from "Loading data..." to "" once the the load_data function has run

## Run the below code if the check is checked ✅
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data.head(10))

st.markdown(" ## Cumulated cases")    

cumulated_cases = pd.DataFrame(data.groupby("month")["cases"].sum()).reset_index()
cumulated_cases["cumulated_cases"] = 0
cumulated_cases.loc[0, "cumulated_cases"] = cumulated_cases.loc[0, "cases"]
for i in range(1, len(cumulated_cases)):
    cumulated_cases.loc[i, "cumulated_cases"] = cumulated_cases.loc[i, "cases"] + cumulated_cases.loc[i-1, "cumulated_cases"]

fig_1 = go.Figure()

fig_1.add_trace(go.Scatter(
    x=cumulated_cases["month"],
    y=cumulated_cases["cumulated_cases"]
))

fig_1.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = [1, 2, 3, 4 , 5, 6, 7, 8, 9, 10, 11, 12],
        ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    )
)

st.plotly_chart(fig_1, use_container_width=True)

st.markdown("""
    ## New cases
""")   

new_cases_global = pd.DataFrame(data.groupby("dateRep")["cases"].sum()).reset_index()
new_cases_global['7_day_avg'] = new_cases_global['cases'].rolling(window=7).mean()

fig_2 = go.Figure()

fig_2.add_trace(go.Scatter(
    x=new_cases_global["dateRep"],
    y=new_cases_global["cases"],
    name="New cases"       
))


fig_2.add_trace(go.Scatter(
    x=new_cases_global["dateRep"],
    y=new_cases_global["7_day_avg"],
    name="7-day average"
))

st.plotly_chart(fig_2, use_container_width=True)

st.markdown("""
    ## Country Analysis
""")

country = st.selectbox("Which country would you like to see?", data["countriesAndTerritories"].sort_values().unique())

cases_deaths_country = data.loc[(data["countriesAndTerritories"]==country), ["dateRep", "cases", "deaths"]]
cases_deaths_country['7_day_cases_avg'] = cases_deaths_country['cases'].rolling(window=7).mean()
cases_deaths_country['7_day_deaths_avg'] = cases_deaths_country['deaths'].rolling(window=7).mean()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Positives cases")
    
    fig_3 = go.Figure()

    fig_3.add_trace(go.Scatter(
        x=cases_deaths_country["dateRep"],
        y=cases_deaths_country["cases"],
        name="New cases"       
    ))


    fig_3.add_trace(go.Scatter(
        x=cases_deaths_country["dateRep"],
        y=cases_deaths_country["7_day_cases_avg"],
        name="7-day average"
    ))

    st.plotly_chart(fig_3, use_container_width=True)

with col2:
    st.markdown("### Deaths")
    
    fig_4 = go.Figure()

    fig_4.add_trace(go.Scatter(
        x=cases_deaths_country["dateRep"],
        y=cases_deaths_country["deaths"],
        name="Deaths"       
    ))


    fig_4.add_trace(go.Scatter(
        x=cases_deaths_country["dateRep"],
        y=cases_deaths_country["7_day_deaths_avg"],
        name="7-day average"
    ))

    st.plotly_chart(fig_4, use_container_width=True)

### Footer 
empty_space, footer = st.columns([1, 2])

with empty_space:
    st.write("")

with footer:
    st.markdown("Made with copy/paste and 💖 by Max")