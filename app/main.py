import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add the 'src' directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

# Now import the data_processing module
from data_processing import (
    load_data,
    calculate_summary_statistics,
    check_data_quality,
    perform_time_series_analysis,
    calculate_correlations,
    analyze_wind_data,
)
# Load data from predefined files
def load_predefined_data(file_name):
    file_path = f"data/{file_name}"  # Adjust path if necessary
    return load_data(file_path)

# Upload user data dynamically
@st.cache_data
def upload_user_data(uploaded_file):
    try:
        return pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# Sidebar for data selection
st.sidebar.title("Data Selection")
data_options = {
    "Benin (Malanville)": "benin-malanville.csv",
    "Sierra Leone (Bumbuna)": "sierraleone-bumbuna.csv",
    "Togo (Dapaong)": "togo-dapaong_qc.csv",
    "Upload Your Own Data": None,
}
selected_data = st.sidebar.selectbox("Choose a dataset:", list(data_options.keys()))

# Handle data loading
if selected_data == "Upload Your Own Data":
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        df = upload_user_data(uploaded_file)
        if df is None:
            st.stop()  # Stop execution if upload fails
        st.sidebar.success("Data uploaded successfully!")
    else:
        st.sidebar.warning("Please upload a CSV file to continue.")
        st.stop()
else:
    df = load_predefined_data(data_options[selected_data])
    st.sidebar.success(f"Loaded {selected_data} dataset.")

# Application Title
st.title("Solar Farm Data Analysis Dashboard")

# Display the dataset
st.header("Dataset Preview")
st.write(df.head())

# Summary Statistics
st.header("Summary Statistics")
try:
    summary_stats = calculate_summary_statistics(df)
    st.write(pd.DataFrame(summary_stats).T)  # Transpose for better display
except Exception as e:
    st.error(f"Error in summary statistics calculation: {e}")

# Data Quality
st.header("Data Quality")
try:
    data_quality = check_data_quality(df)
    st.subheader("Missing Values")
    st.write(pd.Series(data_quality["missing_values"]))
    st.subheader("Outliers")
    st.write(pd.Series(data_quality["outliers"]))
except Exception as e:
    st.error(f"Error in data quality check: {e}")

# Time Series Analysis
st.header("Time Series Analysis")
try:
    time_series_data = perform_time_series_analysis(df)
    fig = go.Figure()
    for var, series in time_series_data.items():
        fig.add_trace(go.Scatter(x=series.index, y=series.values, name=var))
    fig.update_layout(title="Monthly Averages", xaxis_title="Month", yaxis_title="Value")
    st.plotly_chart(fig)
except Exception as e:
    st.error(f"Error in time series analysis: {e}")

# Correlation Analysis
st.header("Correlation Analysis")
try:
    correlations = calculate_correlations(df)
    fig = px.imshow(correlations, text_auto=True, aspect="auto", color_continuous_scale="Viridis")
    fig.update_layout(title="Correlation Heatmap")
    st.plotly_chart(fig)
except Exception as e:
    st.error(f"Error in correlation analysis: {e}")

# Wind Analysis
st.header("Wind Analysis")
try:
    wind_data = analyze_wind_data(df)
    fig1 = px.bar(
        x=wind_data["wind_speed_distribution"].index,
        y=wind_data["wind_speed_distribution"].values,
        labels={"x": "Wind Speed", "y": "Frequency"},
        title="Wind Speed Distribution",
    )
    st.plotly_chart(fig1)

    fig2 = px.bar_polar(
        r=wind_data["wind_direction_distribution"].values,
        theta=wind_data["wind_direction_distribution"].index,
        title="Wind Direction Distribution",
    )
    st.plotly_chart(fig2)
except Exception as e:
    st.error(f"Error in wind analysis: {e}")

# Interactive Feature
st.header("Interactive Data Explorer")
selected_columns = st.multiselect("Select columns to plot", df.select_dtypes(include=["float64", "int64"]).columns)
if selected_columns:
    try:
        fig = px.scatter_matrix(df[selected_columns], title="Scatter Matrix")
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error in interactive data explorer: {e}")

# Display raw data
st.header("Raw Data")
st.write(df)
