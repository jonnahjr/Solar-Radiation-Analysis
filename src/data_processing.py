import pandas as pd
import numpy as np
from typing import Dict, Any


def load_data(file_path: str) -> pd.DataFrame:
    """Load the solar farm data from a CSV file."""
    try:
        df = pd.read_csv(file_path, parse_dates=['Timestamp'])
    except Exception as e:
        raise FileNotFoundError(f"Error loading file at {file_path}: {e}")
    
    # Ensure 'Timestamp' exists and is parsed correctly
    if 'Timestamp' not in df.columns:
        raise ValueError("The 'Timestamp' column is required in the dataset.")
    
    return df


def calculate_summary_statistics(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """Calculate summary statistics for numeric columns."""
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    if numeric_columns.empty:
        raise ValueError("No numeric columns found for summary statistics.")
    
    return {
        col: {
            'mean': df[col].mean(),
            'median': df[col].median(),
            'std': df[col].std(),
            'min': df[col].min(),
            'max': df[col].max(),
        }
        for col in numeric_columns
    }


def check_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
    """Check for missing values and outliers."""
    missing_values = df.isnull().sum().to_dict()
    outliers = {}
    
    for col in df.select_dtypes(include=[np.number]).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers[col] = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
    
    return {'missing_values': missing_values, 'outliers': outliers}


def perform_time_series_analysis(df: pd.DataFrame) -> Dict[str, pd.Series]:
    """Perform basic time series analysis."""
    if 'Timestamp' not in df:
        raise ValueError("The dataset must contain a 'Timestamp' column for time series analysis.")
    
    df['Month'] = df['Timestamp'].dt.month
    monthly_avg = df.groupby('Month')[['GHI', 'DNI', 'DHI', 'Tamb']].mean()
    
    return {
        'monthly_avg_GHI': monthly_avg['GHI'],
        'monthly_avg_DNI': monthly_avg['DNI'],
        'monthly_avg_DHI': monthly_avg['DHI'],
        'monthly_avg_Tamb': monthly_avg['Tamb'],
    }


def calculate_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate correlations between key variables."""
    required_columns = ['GHI', 'DNI', 'DHI', 'Tamb', 'WS', 'RH']
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        raise ValueError(f"Missing required columns for correlation: {missing_cols}")
    
    return df[required_columns].corr()


def analyze_wind_data(df: pd.DataFrame) -> Dict[str, pd.Series]:
    """Analyze wind speed and direction."""
    if 'WS' not in df or 'WD' not in df:
        raise ValueError("The dataset must contain 'WS' (Wind Speed) and 'WD' (Wind Direction) columns.")
    
    wind_speed_distribution = df['WS'].value_counts(normalize=True)
    
    # Bin wind direction into 8 categories (45° each)
    wind_direction_bins = pd.cut(
        df['WD'], bins=np.linspace(0, 360, 9), labels=[
            'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'], include_lowest=True
    )
    wind_direction_distribution = wind_direction_bins.value_counts(normalize=True)
    
    return {
        'wind_speed_distribution': wind_speed_distribution,
        'wind_direction_distribution': wind_direction_distribution,
    }


def main(file_path: str):
    print("Loading data...")
    df = load_data(file_path)
    print("Data loaded successfully.")

    print("Calculating summary statistics...")
    summary_stats = calculate_summary_statistics(df)
    print("Summary statistics calculated.")

    print("Checking data quality...")
    data_quality = check_data_quality(df)
    print("Data quality check complete.")

    print("Performing time series analysis...")
    time_series_analysis = perform_time_series_analysis(df)
    print("Time series analysis complete.")

    print("Calculating correlations...")
    correlations = calculate_correlations(df)
    print("Correlation analysis complete.")

    print("Analyzing wind data...")
    wind_analysis = analyze_wind_data(df)
    print("Wind data analysis complete.")

    print("Data processing complete. Results:")
    print("Summary Stats:", summary_stats)
    print("Data Quality:", data_quality)
    print("Correlations:\n", correlations)
    print("Wind Analysis:", wind_analysis)


if __name__ == "__main__":
    # Replace 'path_to_your_data.csv' with an actual path to a valid CSV file
    main("path_to_your_data.csv")
