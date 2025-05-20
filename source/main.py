import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
import os  # Add this import at the top of the file
from file_loader import load_file  # Import only load_file
from service_flag_tracker import process_service_flags, create_service_flag_checkboxes  # Updated function name
from remote_control_tracker import process_remote_control, create_remote_control_checkboxes  # Updated import statement
from tkinter import ttk  # Import ttk for Treeview
import remote_control_common  # Import thfrom config import selected_pf, selected_service_category
from remote_control_map import SERVICE_TYPE_TABLE
from remote_control_common import parse_option

# 하드코딩된 xlsx 파일 경로
HARDCODED_XLSX_PATH = "sample/5YFB4MDE1RP156769_0115-0315.xlsx"
USE_HARDCODED_XLSX = True  # Flag to toggle between hardcoded xlsx and file dialog

# 전역 변수 선언
data = None  # 원본 데이터
filtered_data = None  # 필터링된 데이터

# Disable buttons initially
def disable_buttons():
    parse_button.config(state="disabled")
    expand_collapse_button.config(state="disabled")

def enable_buttons():
    parse_button.config(state="normal")
    expand_collapse_button.config(state="normal")

# 파일 로드 핸들러 함수
def handle_load_file():
    global data
    try:
        if USE_HARDCODED_XLSX:
            # Load the hardcoded xlsx file
            data = pd.read_excel(HARDCODED_XLSX_PATH)
            file_name = os.path.basename(HARDCODED_XLSX_PATH)
        else:
            # Use file dialog to select a file
            file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
            if not file_path:
                return  # User canceled the file dialog
            data = pd.read_excel(file_path)
            file_name = os.path.basename(file_path)

        if data is not None:
            # Standardize column names
            data.columns = data.columns.str.strip().str.lower()
            csv_path_label.config(text=f"Loaded file: {file_name}")
            enable_buttons()  # Enable buttons after successful file load
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")

# Function to sort DataFrame by datetime column
def sort_by_datetime(dataframe):
    dataframe = dataframe.sort_values(by='datetime', ascending=True)  # Sort in ascending order
    return dataframe

# Add a function to get the selected PF value
def get_selected_pf():
    return pf_var.get()

# Filtering and result output
# Modify apply_filter to use selected_service_category from config
def apply_filter():
    filter_date = date_entry.get()
    filter_reqbody = reqbody_entry.get()
    filter_resbody = resbody_entry.get()

    # Get the selected URL option index
    selected_index = url_var.get()
    selected_pf = get_selected_pf()  # Get the selected PF value

    # print(f"Selected Service Category: {selected_service_category}")

    # Use selected_service_category from config
    try:
        # Common filtering logic for datetime, reqbody, and resbody
        filtered_data = data[
            data['datetime'].astype(str).str.contains(filter_date, na=False) &
            data['reqbody'].str.contains(filter_reqbody, na=False) &
            data['resbody'].str.contains(filter_resbody, na=False, regex=True)
        ]
        filtered_data.columns = filtered_data.columns.str.strip().str.lower()
        filtered_data = sort_by_datetime(filtered_data)

        # Filter data based on selected_service_category and parse_option
        # def filter_by_service_category(row):
        #     option_data = row['reqbody'][:14]  # Assuming the first 14 characters are the option data
        #     parsed_option = parse_option(option_data)
        #     return parsed_option.get("Service Type") == SERVICE_TYPE_TABLE.get(str(selected_service_category), "Unknown")

        # filtered_data = filtered_data[filtered_data.apply(filter_by_service_category, axis=1)]

        # Call specific filtering logic based on the selected index
        if selected_index == 0:  # Service Flag Checker
            return process_service_flags(filtered_data, service_flag_checkbox_vars, service_flag_checkbox_labels)

        elif selected_index == 1:  # Remote Control Checker
            # Pass the selected Service Category to process_remote_control
            return process_remote_control(filtered_data, remote_checkbox_vars, remote_checkbox_labels)

        else:
            messagebox.showinfo("Info", "No specific checker selected.")
            return None

    except Exception as e:
        messagebox.showerror("Error", f"Error occurred during filtering: {e}")
        return None

# Function to display JSON in a tree structure
def display_json_tree(json_data):
    # Create a new window for the JSON tree
    tree_window = tk.Toplevel(root)
    tree_window.title("JSON Viewer")

    # Create a Treeview widget
    tree = ttk.Treeview(tree_window)
    tree.pack(fill="both", expand=True)

    # Recursive function to insert JSON data into the tree
    def insert_json(parent, key, value):
        if isinstance(value, dict):
            node = tree.insert(parent, "end", text=key, open=True)
            for sub_key, sub_value in value.items():
                insert_json(node, sub_key, sub_value)
        elif isinstance(value, list):
            node = tree.insert(parent, "end", text=key, open=True)
            for index, item in enumerate(value):
                insert_json(node, f"[{index}]", item)
        else:
            tree.insert(parent, "end", text=key, values=(value,))

    # Add columns to the Treeview
    tree["columns"] = ("Value",)
    tree.column("#0", width=300, anchor="w")
    tree.column("Value", width=300, anchor="w")
    tree.heading("#0", text="Key")
    tree.heading("Value", text="Value")

    # Insert the JSON data into the tree
    insert_json("", "Root", json_data)

# Update parse_resbody_to_table to populate the Treeview
def parse_resbody_to_table():
    result_df = apply_filter()  # Apply filter and get the result DataFrame
    if result_df is None or result_df.empty:
        messagebox.showwarning("Warning", "No data found after filtering.")
        return

    # Clear previous results in the Treeview
    for item in json_tree.get_children():
        json_tree.delete(item)

    # Convert DataFrame to JSON format
    try:
        result_json = result_df.to_dict(orient="records")  # Convert DataFrame to a list of dictionaries

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
        insert_json("", "Root", result_json)
    except Exception as e:
        messagebox.showerror("Error", f"Error occurred during JSON conversion: {e}")

# GUI creation
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
parse_button = tk.Button(result_button_frame, text="Show Results", command=parse_resbody_to_table)
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
radio_frame.pack(side="top", pady=5, anchor="w")  # Repack the radio frame above the data filter

pf_var = tk.StringVar(value="19PF")  # Default value is 19PF

radio_15pf = tk.Radiobutton(radio_frame, text="15PF", variable=pf_var, value="15PF")
radio_15pf.pack(side="left", padx=5)

radio_19pf = tk.Radiobutton(radio_frame, text="19PF", variable=pf_var, value="19PF")
radio_19pf.pack(side="left", padx=5)

radio_19pf_v2 = tk.Radiobutton(radio_frame, text="19PFv2", variable=pf_var, value="19PFv2")
radio_19pf_v2.pack(side="left", padx=5)

# Disable buttons initially
disable_buttons()

# Left frame for buttons and filters
left_frame = tk.Frame(main_frame)
left_frame.pack(side="left", padx=10, anchor="nw")  # Anchor to top-left

# Filter input fields
tk.Label(left_frame, text="Date Filter (datetime):", font=("Arial", 10), anchor="w").pack(side="top", anchor="w")
date_entry = tk.Entry(left_frame)
date_entry.pack(pady=5, side="top", anchor="w")

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

# Create checkboxes for Service Flag options
service_flag_checkbox_vars, service_flag_checkbox_labels, service_flag_checkbox_frame, service_flag_checkboxes = create_service_flag_checkboxes(left_frame)
service_flag_checkbox_frame.pack(pady=5, side="top", anchor="w")
service_flag_checkbox_frame.pack_forget()  # Hidden by default

# Add a label for Service Flag checkboxes
service_flag_label = tk.Label(left_frame, text="Options:", anchor="w", font=("Arial", 10))
service_flag_label.pack(side="top", anchor="w")
service_flag_label.pack_forget()  # Hidden by default

# Create checkboxes for Remote Control options
remote_checkbox_vars, remote_checkbox_labels, remote_checkboxes = create_remote_control_checkboxes(left_frame)
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

# Add a function to update the selected service category
def update_selected_service_category(*args):
    global selected_service_category
    selected_service_category = service_category_var.get()
    if selected_service_category:
        selected_service_category = selected_service_category.split(")")[0].strip("(")

# Bind the service category dropdown to update the selected service category
service_category_var.trace_add("write", update_selected_service_category)

service_category_label = tk.Label(left_frame, text="Service Category:", anchor="w", font=("Arial", 10))
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