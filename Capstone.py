# create a webapp that displays the daily covid information for a user selected country. get the data from the center for systems science engineering covid dashboard
# users should be able to add countries and select options such as whether to display the daily or cumulative case counts

# run streamlit
# streamlit run "/Users/shaynademick/Downloads/Datasci /Capstone.py"

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load both datasets
cases = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/refs/heads/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")

st.set_page_config(layout="wide")
st.markdown("# Covid-19 Dashboard")
st.markdown("##### How to use: Select one or more countries/regions from the dropdown, select a data type, and then select Daily or Cumulative.")
st.markdown("##### Data is from the Johns Hopkins University Center for Systems Science Engineering's Public COVID-19 Data Archive")

# Sidebar controls
options = cases["Country/Region"].unique()
country = st.sidebar.multiselect("Pick countries", options)
data_type = st.sidebar.radio("Data type", ["Cases", "Deaths"])
display = st.sidebar.radio("Display type", ["Daily", "Cumulative"])

# Pick the right dataset based on user selection
if data_type == "Cases":
    df = cases
else:
    df = deaths

# Filter
filtered = df[df["Country/Region"].isin(country)].copy()
date_cols = filtered.columns[4:]
filtered = filtered.groupby("Country/Region")[date_cols].sum().reset_index()
date_cols = filtered.columns[1:]  # after groupby, date cols start at index 1

if display == "Daily":
    # Compute daily differences
    daily_values = pd.DataFrame(
        np.diff(filtered[date_cols].values),
        columns=date_cols[1:]
    )
    data = pd.concat([filtered["Country/Region"].reset_index(drop=True), daily_values], axis=1)

    # Daily line chart
    if len(country) > 0:
        chart_data = data.melt(id_vars="Country/Region", var_name="Date", value_name="Daily Count")
        chart_data["Date"] = pd.to_datetime(chart_data["Date"])

        fig = px.line(
            chart_data,
            x="Date",
            y="Daily Count",
            color="Country/Region",
            title=f"Daily {data_type} Over Time",
            labels={"Date": "Date", "Daily Count": f"Daily {data_type} (Millions)"}
        )
        fig.update_xaxes(dtick="M6", tickformat="%b %Y")
        fig.update_yaxes(tickformat=".2s")
        st.plotly_chart(fig, use_container_width=True)

else:
    # concatenate the country/region with the date/column 
    data = pd.concat([filtered["Country/Region"].reset_index(drop=True), filtered[date_cols]], axis=1)
    # only last column for the cumulative table 
    last_col = data.columns[-1]
    summary = data[["Country/Region", last_col]].rename(columns={last_col: f"Total {data_type} as of {last_col}"})
    st.markdown("## Latest data")
    st.write(summary)

    if len(country) > 0:
        chart_data = data.melt(id_vars="Country/Region", var_name="Date", value_name="Cumulative Count")
        chart_data["Date"] = pd.to_datetime(chart_data["Date"])

        fig = px.line(
            chart_data,
            x="Date",
            y="Cumulative Count",
            color="Country/Region",
            title=f"Cumulative {data_type} Over Time",
            labels={"Date": "Year", "Cumulative Count": f"Cumulative {data_type}"}
        )
        fig.update_xaxes(dtick="M12", tickformat="%Y")
        fig.update_yaxes(tickformat=".2s")
        st.plotly_chart(fig, use_container_width=True)


st.write(data)

    # code wAAI CLAUDE

    # charts wWAI CLAUDE
    # rest of code wAAI CLAUDE
