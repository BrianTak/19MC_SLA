import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar
import xml.etree.ElementTree as ET
import os  # Add this import at the top of the file
import numpy as np  # Import numpy as np
from util.file_loader import load_file  # Import only load_file
from service_flag.service_flag_tracker import process_service_flags  # Updated function name
from remote_control.remote_control_tracker import process_remote_control  # Updated import statement
from tkinter import ttk  # Import ttk for Treeview
from remote_control.remote_control_map import SERVICE_TYPE_TABLE
from remote_control.remote_control_common import parse_option
from util.config import (
    SERVICE_FLAG_URL,
    RSCDLCHK_URL,
    REMOTE_CONTROL_CMD_URL,
    REMOTE_CONTROL_RESP_URL,
    CHECKBOX_LABELS,
    get_selected_pf,
    set_selected_pf,
    set_selected_service_category,
    set_selected_service_flags,
)
from util.database import (
    get_original_data,
    set_original_data,
    get_filtered_data,
    set_filtered_data,
    init_filtered_data,
    set_filtered_data_by_date,
    set_filtered_data_by_urls,
    set_filtered_data_by_reqbody_str,
    set_filtered_data_by_resbody_str
)

# 하드코딩된 xlsx 파일 경로
HARDCODED_XLSX_PATH = "sample/5YFB4MDE1RP156769_0115-0315.xlsx"
USE_HARDCODED_XLSX = True  # Flag to toggle between hardcoded xlsx and file dialog

# Disable buttons initially
def disable_buttons():
    parse_button.config(state="disabled")
    expand_collapse_button.config(state="disabled")

def enable_buttons():
    parse_button.config(state="normal")
    expand_collapse_button.config(state="normal")

# 파일 로드 핸들러 함수
def handle_load_file():
    try:
        if USE_HARDCODED_XLSX:
            # Load the hardcoded xlsx file
            set_original_data(pd.read_excel(HARDCODED_XLSX_PATH))
            file_name = os.path.basename(HARDCODED_XLSX_PATH)
        else:
            # Use file dialog to select a file
            file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
            if not file_path:
                return  # User canceled the file dialog
            set_original_data(pd.read_excel(file_path))
            file_name = os.path.basename(file_path)

        if get_original_data() is not None:
            csv_path_label.config(text=f"Loaded file: {file_name}")
            enable_buttons()  # Enable buttons after successful file load
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")

# Filtering and result output
# Modify apply_filter to use selected_service_category from util.config
def apply_filter():
    filter_start_date = start_date_var.get()
    filter_end_date = end_date_var.get()
    filter_reqbody = reqbody_entry.get()
    filter_resbody = resbody_entry.get()

    # Get the selected URL option index
    selected_index = url_var.get()

    # Use selected_service_category from util.config
    try:
        set_filtered_data(pd.DataFrame(get_original_data()))
        init_filtered_data()

        # Apply date range filtering if both start and end dates are provided
        if filter_start_date or filter_end_date:
            set_filtered_data_by_date(filter_start_date, filter_end_date)

        set_filtered_data_by_reqbody_str(filter_reqbody)
        set_filtered_data_by_resbody_str(filter_resbody)

        # Call populate_date_dropdowns after filtering
        populate_date_dropdowns()

        # Call specific filtering logic based on the selected index
        if selected_index == 0:  # Service Flag Checker
            selected_checkboxes = [
                label for var, label in zip(service_flag_checkbox_vars, CHECKBOX_LABELS) if var.get()
            ] or CHECKBOX_LABELS
            set_filtered_data_by_urls([SERVICE_FLAG_URL, RSCDLCHK_URL])
            set_selected_service_flags(selected_checkboxes)
            return process_service_flags()

        elif selected_index == 1:  # Remote Control Checker
            selected_urls = [
                url for var, label, url in zip(remote_checkbox_vars, remote_checkbox_labels,
                [REMOTE_CONTROL_CMD_URL, REMOTE_CONTROL_RESP_URL]) if var.get()
            ] or [REMOTE_CONTROL_CMD_URL, REMOTE_CONTROL_RESP_URL]
            set_filtered_data_by_urls(selected_urls)

            # Get the selected service category from the dropdown
            selected_service_category = service_category_var.get().split(")")[0].strip("(")
            set_selected_service_category(selected_service_category)

            # Call process_remote_control
            return process_remote_control()

        else:
            messagebox.showinfo("Info", "No specific checker selected.")
            return None

    except Exception as e:
        messagebox.showerror("Error", f"Error occurred during filtering: {e}")
        return None

# Update show_result to populate the Treeview
def show_result():
    # Clear previous results in the Treeview
    for item in json_tree.get_children():
        json_tree.delete(item)

    result_df = apply_filter()  # Apply filter and get the result DataFrame
    if result_df is None or result_df.empty:
        messagebox.showwarning("Warning", "No data found after filtering.")
        return

    # Convert DataFrame to JSON format without NaN values
    try:
        result_json = result_df.to_dict(orient="records")

        # Recursive function to insert JSON data into the Treeview
        def insert_json(parent, key, value):
            if isinstance(value, dict):
                node = json_tree.insert(parent, "end", text=key, open=False)  # Set open=False for collapsed state
                for sub_key, sub_value in value.items():
                    insert_json(node, sub_key, sub_value)
            elif isinstance(value, list):
                node = json_tree.insert(parent, "end", text=key, open=False)  # Set open=False for collapsed state
                for index, item in enumerate(value):
                    insert_json(node, f"[{index}]", item)
            else:
                json_tree.insert(parent, "end", text=key, values=(value,))

        # Insert the JSON data into the Treeview
        insert_json("", "Result", result_json)
    except Exception as e:
        messagebox.showerror("Error", f"Error occurred during JSON conversion: {e}")

# GUI creation
# Initialize Tkinter root window
root = tk.Tk()

root.title("Totoya 19MC Server Log Analyzer")

# Main frame for horizontal layout
main_frame = tk.Frame(root)
main_frame.pack(pady=10, padx=10, anchor="nw")  # Anchor to top-left

# Top frame for CSV and result buttons
top_frame = tk.Frame(main_frame)
top_frame.pack(side="top", pady=10, fill="x", anchor="w")  # Place it above the left_frame

# Frame for CSV load button and file name label
csv_frame = tk.Frame(top_frame)
csv_frame.pack(pady=5, fill="x", anchor="w")  # Pack the frame in the top_frame

# CSV file load button
load_button = tk.Button(csv_frame, text="Load File", command=handle_load_file)
load_button.pack(side="left", padx=5, anchor="w")  # Left-align the button

# CSV file path display label
csv_path_label = tk.Label(csv_frame, text="Loaded file: None", font=("Arial", 10), anchor="w")
csv_path_label.pack(side="left", padx=5, fill="x", expand=True, anchor="w")  # Left-align the label

# Frame for the result output button
result_button_frame = tk.Frame(top_frame)
result_button_frame.pack(pady=5, fill="x", anchor="w")  # Place it below the csv_frame

# Result output button
parse_button = tk.Button(result_button_frame, text="Show Results", command=show_result)
parse_button.pack(side="left", padx=5, anchor="w")  # Left-align the button

# Add a toggle button to control the open/close state of the JSON tree

def toggle_json_tree_expand_collapse():
    """Toggle the open/close state of all nodes in the JSON tree."""
    def toggle_node(node, open_state):
        json_tree.item(node, open=open_state)
        for child in json_tree.get_children(node):
            toggle_node(child, open_state)

    # Determine the current state of the root node
    root_node = json_tree.get_children()
    if root_node:
        current_state = json_tree.item(root_node[0], "open")
        new_state = not current_state
        for node in root_node:
            toggle_node(node, new_state)

# Rename the toggle button to "Expand/Collapse JSON Tree"
expand_collapse_button = tk.Button(result_button_frame, text="Expand/Collapse", command=toggle_json_tree_expand_collapse)
expand_collapse_button.pack(side="left", padx=5, anchor="w")

# Add radio buttons next to the expand button for 15PF and 19PF options
radio_frame = tk.Frame(result_button_frame)
radio_frame.pack_forget()  # Remove the radio frame from its current position
radio_frame.pack(side="left", pady=5, anchor="w")  # Repack the radio frame above the data filter

pf_options = ["15PF", "19PF", "19PFv2"]

# tk.Label(left_frame, text="PF Filter:", font=("Arial", 10), anchor="w").pack(side="top", anchor="w")
pf_var = tk.IntVar(value=1)  # Default value is the index of the first option
set_selected_pf(pf_options[pf_var.get()])

for index, option in enumerate(pf_options):
    tk.Radiobutton(radio_frame, text=option, variable=pf_var, value=index, anchor="w").pack(side="left", anchor="w")

pf_var.trace_add("write", lambda *args: (set_selected_pf(pf_options[pf_var.get()]), print(f"selected_pf: {get_selected_pf()}")))

# Disable buttons initially
disable_buttons()

# Left frame for buttons and filters
left_frame = tk.Frame(main_frame)
left_frame.pack(side="left", padx=10, anchor="nw")  # Anchor to top-left

# Filter input fields
# Add start_date and end_date entries for date range filtering
# Add a dropdown for Start Date
tk.Label(left_frame, text="Start Date (datetime):", font=("Arial", 10), anchor="w").pack(side="top", anchor="w")
start_date_var = tk.StringVar(value=None)
start_date_dropdown = ttk.Combobox(left_frame, textvariable=start_date_var, state="readonly")
start_date_dropdown.pack(pady=5, side="top", anchor="w")

# Add a dropdown for End Date
tk.Label(left_frame, text="End Date (datetime):", font=("Arial", 10), anchor="w").pack(side="top", anchor="w")
end_date_var = tk.StringVar(value=None)
end_date_dropdown = ttk.Combobox(left_frame, textvariable=end_date_var, state="readonly")
end_date_dropdown.pack(pady=5, side="top", anchor="w")

# Function to populate the dropdowns with unique datetime values from get_filtered_data()
def populate_date_dropdowns():
    try:
        data = get_filtered_data()
        if data is not None and not data.empty:
            unique_dates = sorted(data['datetime'].dropna().unique())
            start_date_dropdown['values'] = unique_dates
            end_date_dropdown['values'] = unique_dates
    except Exception as e:
        messagebox.showerror("Error", f"Failed to populate date dropdowns: {e}")

url_options = [
    "Service Flag",
    "Remote Control"
]

# URL filter (Radio Buttons)
tk.Label(left_frame, text="URL Filter:", font=("Arial", 10), anchor="w").pack(side="top", anchor="w")
url_var = tk.IntVar(value=0)  # Default value is the index of the first option

for index, option in enumerate(url_options):
    tk.Radiobutton(left_frame, text=option, variable=url_var, value=index, anchor="w").pack(side="top", anchor="w")

# ReqBody filter
reqbody_label = tk.Label(left_frame, text="ReqBody Filter:", font=("Arial", 10), anchor="w")
reqbody_label.pack(side="top", anchor="w")
reqbody_entry = tk.Entry(left_frame)
reqbody_entry.pack(pady=5, side="top", anchor="w")
reqbody_label.pack_forget()  # Hidden by default
reqbody_entry.pack_forget()  # Hidden by default

# ResBody filter
resbody_label = tk.Label(left_frame, text="ResBody Filter:", font=("Arial", 10), anchor="w")
resbody_label.pack(side="top", anchor="w")
resbody_entry = tk.Entry(left_frame)
resbody_entry.pack(pady=5, side="top", anchor="w")
resbody_label.pack_forget()  # Hidden by default
resbody_entry.pack_forget()  # Hidden by default

# Add a label for Service Flag checkboxes
service_flag_label = tk.Label(left_frame, text="Options:", anchor="w", font=("Arial", 10))

# Create a frame for Service Flag checkboxes
service_flag_checkbox_frame = tk.Frame(left_frame)
service_flag_checkbox_vars = []
service_flag_checkboxes = []

for label in CHECKBOX_LABELS:
    var = tk.BooleanVar(value=(label in ["Telematics"]))  # Default check for Telematics and RSFlag
    service_flag_checkbox_vars.append(var)
    cb = tk.Checkbutton(service_flag_checkbox_frame, text=label, variable=var)
    service_flag_checkboxes.append(cb)

# Pack the frame and label, but hide them by default
service_flag_checkbox_frame.pack(pady=5, side="top", anchor="w")
service_flag_checkbox_frame.pack_forget()  # Hidden by default
service_flag_label.pack(side="top", anchor="w")
service_flag_label.pack_forget()  # Hidden by default

# Create checkboxes for Remote Control options
remote_checkbox_vars = []
remote_checkbox_labels = ["rmtctrlcmd", "resrmtctrl"]
remote_checkboxes = []

for label in remote_checkbox_labels:
    var = tk.BooleanVar(value=False)
    remote_checkbox_vars.append(var)
    checkbox = tk.Checkbutton(left_frame, text=label, variable=var)
    remote_checkboxes.append(checkbox)
    checkbox.pack(anchor="w")

remote_control_label = tk.Label(left_frame, text="Options:", anchor="w", font=("Arial", 10))
remote_control_label.pack(side="top", anchor="w")
remote_control_label.pack_forget()  # Initially hidden
for cb in remote_checkboxes:
    cb.pack(side="top", anchor="w")  # Initially hide the checkboxes
    cb.pack_forget()

# Add a dropdown for Service Category
service_category_var = tk.StringVar()

# Extract keys and values from SERVICE_TYPE_TABLE for the dropdown options
service_category_keys = list(SERVICE_TYPE_TABLE.keys())
service_category_values = list(SERVICE_TYPE_TABLE.values())

# Set the default value of service_category_var to the first key-value pair in SERVICE_TYPE_TABLE
if service_category_keys:
    service_category_var.set(f"({service_category_keys[0]}) {service_category_values[0]}")

# Update the dropdown to use the extracted keys and values
service_category_dropdown = tk.OptionMenu(left_frame, service_category_var, *[f"({key}) {value}" for key, value in SERVICE_TYPE_TABLE.items()])
service_category_dropdown.pack_forget()  # Initially hidden

# Bind the service category dropdown to update the selected service category
service_category_var.trace_add("write", lambda *args: (set_selected_service_category(service_category_var.get().split(")")[0].strip("(")), print(f"Selected Service Category Key: {service_category_var.get().split(')')[0].strip('(')}")))

service_category_label = tk.Label(left_frame, text="Service Category Filter:", anchor="w", font=("Arial", 10))
service_category_label.pack_forget()  # Initially hidden

# Right frame for result output
right_frame = tk.Frame(main_frame)
# right_frame.config(highlightbackground="black", highlightthickness=1)
right_frame.pack(side="right", padx=10, fill="both", expand="true", anchor="nw")  # Anchor to top-left

# Update all child frames to fill parent and be responsive
for child in right_frame.winfo_children():
    child.pack(anchor="nw")  # Anchor to top-left

# Result output in the right frame
result_label = tk.Label(right_frame, text="Console:", font=("Arial", 10, "bold"))
result_label.pack(anchor="nw")

# Repack the result_text widget and scrollbars into a dedicated frame
result_frame = tk.Frame(right_frame)
result_frame.pack(fill="both", expand="true", anchor="nw")  # Anchor to top-left

# Replace result_text with a JSON viewer using Treeview
# Remove the result_text widget and its scrollbars
json_tree = ttk.Treeview(result_frame)

# Add scrollbars to the JSON Treeview
json_tree_scroll_y = tk.Scrollbar(result_frame, orient="vertical", command=json_tree.yview)
json_tree_scroll_x = tk.Scrollbar(result_frame, orient="horizontal", command=json_tree.xview)
json_tree.configure(yscrollcommand=json_tree_scroll_y.set, xscrollcommand=json_tree_scroll_x.set)

# Adjust layout to include scrollbars using grid
json_tree.grid(row=0, column=0, sticky="nsew")
json_tree_scroll_y.grid(row=0, column=1, sticky="ns")
json_tree_scroll_x.grid(row=1, column=0, sticky="ew")

# Configure the grid to allow resizing
result_frame.grid_rowconfigure(0, weight=1)
result_frame.grid_columnconfigure(0, weight=1)

# Increase the size of the result frame by 30%
root.update_idletasks()  # Ensure the window is fully rendered before resizing
result_frame.config(width=int(root.winfo_width() * 0.7), height=int(root.winfo_height() * 0.7))

# Add columns to the Treeview
json_tree["columns"] = ("Value",)
json_tree.column("#0", minwidth=150, width=500, stretch=True, anchor="w")  # Adjust column width and allow stretching
json_tree.column("Value", minwidth=150, width=500, stretch=True, anchor="w")  # Adjust column width and allow stretching
json_tree.heading("#0", text="Key", anchor="w")  # Align heading to the left
json_tree.heading("Value", text="Value", anchor="w")  # Align heading to the left

# Set the height of the json_tree to 150
json_tree.config(height=30)

# Define update_visibility after result_text is defined
def update_visibility(*args):
    # Clear the Treeview content when the radio button is changed
    for item in json_tree.get_children():
        json_tree.delete(item)

    if url_var.get() == 0:  # "Service Flag Checker" is selected
        reqbody_label.pack_forget()
        reqbody_entry.pack_forget()
        resbody_label.pack_forget()
        resbody_entry.pack_forget()
        service_flag_label.pack(anchor="w")  # Show Service Flag label
        service_flag_checkbox_frame.pack(pady=5, anchor="w")
        for cb in service_flag_checkboxes:
            cb.pack(anchor="w")
        remote_control_label.pack_forget()  # Hide Remote Control label
        for cb in remote_checkboxes:
            cb.pack_forget()  # Hide remote control checkboxes
        service_category_label.pack_forget()  # Hide Service Category label
        service_category_dropdown.pack_forget()  # Hide Service Category dropdown
    elif url_var.get() == 1:  # "Remote Control Checker" is selected
        reqbody_label.pack_forget()
        reqbody_entry.pack_forget()
        resbody_label.pack_forget()
        resbody_entry.pack_forget()
        service_flag_label.pack_forget()  # Hide Service Flag label
        service_flag_checkbox_frame.pack_forget()
        for cb in service_flag_checkboxes:
            cb.pack_forget()  # Hide service flag checkboxes
        remote_control_label.pack(anchor="w")  # Show Remote Control label
        for cb in remote_checkboxes:
            cb.pack(anchor="w")  # Show remote control checkboxes
        service_category_label.pack(anchor="w")  # Show Service Category label
        service_category_dropdown.pack(anchor="w")  # Show Service Category dropdown
    else:  # Other options are selected
        reqbody_label.pack(anchor="w")
        reqbody_entry.pack(pady=5, anchor="w")
        resbody_label.pack(anchor="w")
        resbody_entry.pack(pady=5, anchor="w")
        service_flag_label.pack_forget()  # Hide Service Flag label
        service_flag_checkbox_frame.pack_forget()
        for cb in service_flag_checkboxes:
            cb.pack_forget()  # Hide service flag checkboxes
        remote_control_label.pack_forget()  # Hide Remote Control label
        for cb in remote_checkboxes:
            cb.pack_forget()  # Hide remote control checkboxes
        service_category_label.pack_forget()  # Hide Service Category label
        service_category_dropdown.pack_forget()  # Hide Service Category dropdown
        service_flag_label.pack_forget()  # Hide Service Flag label
        service_flag_checkbox_frame.pack_forget()
        for cb in service_flag_checkboxes:
            cb.pack_forget()  # Hide service flag checkboxes
        remote_control_label.pack_forget()  # Hide Remote Control label
        for cb in remote_checkboxes:
            cb.pack_forget()  # Hide remote control checkboxes

# Bind the URL filter variable to update visibility
url_var.trace_add("write", update_visibility)

# Initialize visibility based on the default URL filter
update_visibility()

# Run the GUI
root.mainloop()