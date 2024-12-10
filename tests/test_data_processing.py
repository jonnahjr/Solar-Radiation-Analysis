import pytest
import os
import pandas as pd
from src.data_processing import load_data, calculate_summary_statistics

# Set up test data file path
TEST_DATA_FILE = 'data/test_data.csv'

@pytest.fixture
def test_data():
    # Create a fixture to load test data for multiple tests
    if not os.path.exists(TEST_DATA_FILE):
        pytest.fail(f"Test data file not found: {TEST_DATA_FILE}")
    return load_data(TEST_DATA_FILE)

def test_load_data():
    # Test loading data
    data = load_data(TEST_DATA_FILE)
    assert isinstance(data, pd.DataFrame), "Loaded data should be a DataFrame"
    assert not data.empty, "DataFrame should not be empty"

def test_calculate_summary_stats(test_data):
    # Test summary statistics calculation
    summary = calculate_summary_statistics(test_data)
    assert isinstance(summary, pd.DataFrame), "Summary statistics should be a DataFrame"
    assert not summary.empty, "Summary statistics DataFrame should not be empty"
    assert 'mean' in summary.columns, "Summary should include 'mean' as a column"
