import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data_processing import (
    load_data,
    calculate_summary_statistics,
    check_data_quality,
    perform_time_series_analysis,
    calculate_correlations,
    analyze_wind_data
)

# Load data
@st.cache_data
def get_data():
    return load_data("path_to_your_data.csv")

df = get_data()

st.title("Solar Farm Data Analysis Dashboard")

# Summary Statistics
st.header("Summary Statistics")
summary_stats = calculate_summary_statistics(df)
st.write(pd.DataFrame(summary_stats))

# Data Quality
st.header("Data Quality")
data_quality = check_data_quality(df)
st.subheader("Missing Values")
st.write(pd.Series(data_quality['missing_values']))
st.subheader("Outliers")
st.write(pd.Series(data_quality['outliers']))

# Time Series Analysis
st.header("Time Series Analysis")
time_series_data = perform_time_series_analysis(df)
fig = go.Figure()
for var in time_series_data:
    fig.add_trace(go.Scatter(x=time_series_data[var].index, y=time_series_data[var].values, name=var))
fig.update_layout(title="Monthly Averages", xaxis_title="Month", yaxis_title="Value")
st.plotly_chart(fig)

# Correlation Analysis
st.header("Correlation Analysis")
correlations = calculate_correlations(df)
fig = px.imshow(correlations, text_auto=True, aspect="auto")
fig.update_layout(title="Correlation Heatmap")
st.plotly_chart(fig)

# Wind Analysis
st.header("Wind Analysis")
wind_data = analyze_wind_data(df)
fig = px.bar(x=wind_data['wind_speed_distribution'].index, y=wind_data['wind_speed_distribution'].values)
fig.update_layout(title="Wind Speed Distribution", xaxis_title="Wind Speed", yaxis_title="Frequency")
st.plotly_chart(fig)

fig = px.bar_polar(r=wind_data['wind_direction_distribution'].values, theta=wind_data['wind_direction_distribution'].index)
fig.update_layout(title="Wind Direction Distribution")
st.plotly_chart(fig)

# Interactive Feature
st.header("Interactive Data Explorer")
selected_columns = st.multiselect("Select columns to plot", df.select_dtypes(include=['float64', 'int64']).columns)
if selected_columns:
    fig = px.scatter_matrix(df[selected_columns])
    st.plotly_chart(fig)

st.header("Raw Data")
st.write(df)

