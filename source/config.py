from tkinter import StringVar

global selected_pf

# Define selected_pf as a global variable
selected_pf = "19PF"

# Getter and Setter for selected_pf
def get_selected_pf():
    global selected_pf
    return selected_pf

def set_selected_pf(value):
    global selected_pf
    selected_pf = value

selected_service_category = "00"

# Getter and Setter for selected_service_category
def get_selected_service_category():
    global selected_service_category
    return selected_service_category

def set_selected_service_category(value):
    global selected_service_category
    selected_service_category = value

REMOTE_CONTROL_CMD_URL = "http://dcmservice-remocon-service.local/remoteservices/rmtctrlcmd/"
REMOTE_CONTROL_RESP_URL = "http://dcmservice-remocon-service.local/mc/remoteservices/resrmtctrl/"

URL_NAME_MAPPING = {
    REMOTE_CONTROL_CMD_URL: "rmtctrlcmd",
    REMOTE_CONTROL_RESP_URL: "resrmtctrl"
}

original_data = None
filtered_data = None

def get_original_data():
    global original_data
    return original_data

def set_original_data(data):
    global original_data
    original_data = data

# Getter and Setter for filtered_data
def get_filtered_data():
    global filtered_data
    return filtered_data

def set_filtered_data(value):
    global filtered_data
    filtered_data = value

def clear_filtered_data():
    global filtered_data
    filtered_data = original_data

def init_filtered_data():
    global filtered_data
    if filtered_data is not None:
        filtered_data = filtered_data.sort_values(by=['datetime'], ascending=False)
        filtered_data.columns.str.strip().str.lower()

def set_filtered_data_by_date(value):
    global filtered_data
    if filtered_data is not None:
        filtered_data[filtered_data['datetime'].astype(str).str.contains(value, na=False)]

def set_filtered_data_by_urls(value):
    global filtered_data
    if filtered_data is not None:
        filtered_data[filtered_data['url'].isin(value)]
