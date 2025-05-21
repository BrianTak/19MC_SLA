import pandas as pd

from config import (
    REMOTE_CONTROL_CMD_URL,
    REMOTE_CONTROL_RESP_URL
)

original_data = None
filtered_data = None

def get_original_data():
    global original_data
    return original_data

def set_original_data(data):
    global original_data
    original_data = data
    if isinstance(data, pd.DataFrame):
        original_data = data
    else:
        raise ValueError("filtered_data must be a pandas DataFrame")

# Getter and Setter for filtered_data
def get_filtered_data():
    global filtered_data
    return filtered_data

# Ensure filtered_data is always a pandas DataFrame
def set_filtered_data(data):
    global filtered_data
    if isinstance(data, pd.DataFrame):
        filtered_data = data
    else:
        raise ValueError("filtered_data must be a pandas DataFrame")

# Update init_filtered_data to ensure filtered_data remains a DataFrame
def init_filtered_data():
    global filtered_data
    if isinstance(filtered_data, pd.DataFrame):
        filtered_data = filtered_data.sort_values(by=['datetime'], ascending=True)
        filtered_data.columns = filtered_data.columns.str.strip().str.lower()
    else:
        raise ValueError("filtered_data must be a pandas DataFrame")

# Update set_filtered_data_by_date to ensure filtered_data remains a DataFrame
def set_filtered_data_by_date(start_date=None, end_date=None):
    global filtered_data
    if isinstance(filtered_data, pd.DataFrame):
        if start_date and end_date:
            filtered_data = filtered_data[(filtered_data['datetime'] >= start_date) & (filtered_data['datetime'] <= end_date)]
        elif start_date:
            filtered_data = filtered_data[filtered_data['datetime'] >= start_date]
        elif end_date:
            filtered_data = filtered_data[filtered_data['datetime'] <= end_date]
    else:
        raise ValueError("filtered_data must be a pandas DataFrame")

# Update set_filtered_data_by_urls to ensure filtered_data remains a DataFrame
def set_filtered_data_by_urls(value):
    global filtered_data
    if isinstance(filtered_data, pd.DataFrame):
        filtered_data = filtered_data[filtered_data['url'].isin(value)]
    else:
        raise ValueError("filtered_data must be a pandas DataFrame")

# Update set_filtered_data_by_reqbody_str to ensure filtered_data remains a DataFrame
def set_filtered_data_by_reqbody_str(value):
    global filtered_data
    if isinstance(filtered_data, pd.DataFrame):
        filtered_data = filtered_data[filtered_data['reqbody'].str.contains(value, na=False)]
    else:
        raise ValueError("filtered_data must be a pandas DataFrame")

# Update set_filtered_data_by_resbody_str to ensure filtered_data remains a DataFrame
def set_filtered_data_by_resbody_str(value):
    global filtered_data
    if isinstance(filtered_data, pd.DataFrame):
        filtered_data = filtered_data[filtered_data['resbody'].str.contains(value, na=False)]
    else:
        raise ValueError("filtered_data must be a pandas DataFrame")

# Update set_filtered_data_by_service_flag to ensure filtered_data remains a DataFrame
def set_filtered_data_by_service_flag(flag):
    global filtered_data
    if isinstance(filtered_data, pd.DataFrame):
        filtered_data = filtered_data[filtered_data['service_flag'] == flag]
    else:
        raise ValueError("filtered_data must be a pandas DataFrame")
