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

# Add a global variable for filtered_data
filtered_data = None

# Getter and Setter for filtered_data
def get_filtered_data():
    global filtered_data
    return filtered_data

def set_filtered_data(value):
    global filtered_data
    filtered_data = value