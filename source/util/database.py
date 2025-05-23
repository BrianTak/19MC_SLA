import pandas as pd

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

# Update set_filtered_data_by_urls to ensure filtered_data remains a DataFrame
def set_filtered_data_by_urls(value):
    global filtered_data
    if isinstance(filtered_data, pd.DataFrame):
        filtered_data = filtered_data[filtered_data['url'].isin(value)]
        filtered_data.columns = filtered_data.columns.str.strip().str.lower()
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


global filtered_json

def get_filtered_json():
    global filtered_json
    return filtered_json

# Update set_filtered_data_by_date to ensure filtered_data remains a DataFrame
def set_filtered_json_by_date(start_date=None, end_date=None):
    global filtered_json
    global filtered_data

    filtered_json = filtered_data.copy()
    filtered_json.columns = filtered_json.columns.str.strip().str.lower()  # Strip whitespace from column names

    if (start_date and end_date) and start_date >= end_date:
        raise ValueError("start_date must be less than end_date")

    if isinstance(filtered_json, pd.DataFrame):
        if start_date and end_date:
            filtered_json = filtered_json[(filtered_json['datetime'] >= start_date) & (filtered_json['datetime'] <= end_date)]
        elif start_date:
            filtered_json = filtered_json[filtered_json['datetime'] >= start_date]
        elif end_date:
            filtered_json = filtered_json[filtered_json['datetime'] <= end_date]
    else:
        raise ValueError("filtered_data must be a pandas DataFrame")

    return filtered_json