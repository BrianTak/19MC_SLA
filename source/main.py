import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk
from service_flag.service_flag_tracker import process_service_flags  # Updated function name
from remote_control.remote_control_tracker import process_remote_control  # Updated import statement
from remote_control.remote_control_map import SERVICE_TYPE_TABLE

from util.file_loader import (
    handle_load_file,
)

from util.config import (
    SERVICE_FLAG_URL,
    RSCDLCHK_URL,
    REMOTE_CONTROL_CMD_URL,
    REMOTE_CONTROL_RESP_URL,
    SERVICE_FLAG_LABELS,
    PLATFORM_LABELS,
    URL_LABELS,
    REMOTE_CONTROL_LABELS,
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
    set_filtered_data_by_urls,
    set_filtered_data_by_reqbody_str,
    set_filtered_data_by_resbody_str,
    get_filtered_json,
    set_filtered_json_by_date,
)

def apply_filter_on_data():
    filter_reqbody = get_reqbody_entry()
    filter_resbody = get_resbody_entry()

    # Get the selected URL option index
    selected_index = get_url_var()

    # Use selected_service_category from util.config
    try:
        set_filtered_data(pd.DataFrame(get_original_data()))
        init_filtered_data()

        set_filtered_data_by_reqbody_str(filter_reqbody)
        set_filtered_data_by_resbody_str(filter_resbody)

        # Call specific filtering logic based on the selected index
        if selected_index == 0:  # Service Flag Checker
            selected_checkboxes = [
                label for var, label in zip(get_service_flag_checkbox_vars(), SERVICE_FLAG_LABELS) if var.get()
            ] or SERVICE_FLAG_LABELS
            set_filtered_data_by_urls([SERVICE_FLAG_URL, RSCDLCHK_URL])
            set_selected_service_flags(selected_checkboxes)

            set_filtered_data(process_service_flags())
            return get_filtered_data()

        elif selected_index == 1:  # Remote Control Checker
            selected_urls = [
                url for var, url in zip(get_remote_control_vars(),
                [REMOTE_CONTROL_CMD_URL, REMOTE_CONTROL_RESP_URL]) if var.get()
            ] or [REMOTE_CONTROL_CMD_URL, REMOTE_CONTROL_RESP_URL]
            set_filtered_data_by_urls(selected_urls)

            # Get the selected service category from the dropdown
            selected_service_category = get_service_category_var().split(")")[0].strip("(")
            set_selected_service_category(selected_service_category)

            set_filtered_data(process_remote_control())
            return get_filtered_data()

        else:
            messagebox.showinfo("Info", "No specific checker selected.")
            return None

    except Exception as e:
        messagebox.showerror("Error", f"Error occurred during filtering: {e}")
        return None

# Function to populate the dropdowns with unique datetime values from get_filtered_data()
def populate_date_dropdowns():
    data = pd.DataFrame(get_filtered_data())
    # Ensure the 'datetime' column exists in the data
    data.columns = data.columns.str.strip().str.lower()  # Strip whitespace from column names
    if "datetime" in data.columns:
        unique_dates = sorted(data["datetime"].dropna().unique())
        start_date_dropdown["values"] = unique_dates
        end_date_dropdown["values"] = unique_dates
    else:
        messagebox.showwarning("Warning", "'datetime' column not found in the data.")

def apply_filter_on_json():
    # Call populate_date_dropdowns after filtering
    populate_date_dropdowns()

    filter_start_date = get_start_date_var()
    filter_end_date = get_end_date_var()

    try:
        set_filtered_json_by_date(filter_start_date, filter_end_date)
    except Exception as e:
        messagebox.showerror("Error", f"Error occurred while applying date filter: {e}")

    return get_filtered_json()

# Update show_result to populate the Treeview
def show_result():
    # Clear previous results in the Treeview
    for item in get_json_tree().get_children():
        get_json_tree().delete(item)

    result_data = apply_filter_on_data()
    if result_data is None or result_data.empty:
        messagebox.showwarning("Warning", "No database found after filtering.")
        return

    result_json = apply_filter_on_json()
    # Check if the DataFrame is empty after filtering
    if result_json.empty or not result_json.values.tolist():
        messagebox.showwarning("Warning", "No json found after filtering.")
        return

    # Convert DataFrame to JSON format without NaN values
    try:
        result = result_json.to_dict(orient="records")

        # Recursive function to insert JSON data into the Treeview
        def insert_json(parent, key, value):
            if isinstance(value, dict):
                node = get_json_tree().insert(parent, "end", text=key, open=False)  # Set open=False for collapsed state
                for sub_key, sub_value in value.items():
                    insert_json(node, sub_key, sub_value)
            elif isinstance(value, list):
                node = get_json_tree().insert(parent, "end", text=key, open=False)  # Set open=False for collapsed state
                for index, item in enumerate(value):
                    insert_json(node, f"[{index}]", item)
            else:
                get_json_tree().insert(parent, "end", text=key, values=(value,))

        # Insert the JSON data into the Treeview
        insert_json("", "Result", result)
    except Exception as e:
        messagebox.showerror("Error", f"Error occurred during JSON conversion: {e}")

# GUI creation
# Initialize Tkinter root window
def create_root_window():
    root = tk.Tk()
    root.title("Totoya 19MC Server Log Analyzer")
    return root

def create_main_frame(root):
    main_frame = tk.Frame(root)
    main_frame.pack(pady=10, padx=10, anchor="nw")
    return main_frame

def create_top_frame(main_frame):
    top_frame = tk.Frame(main_frame)
    top_frame.pack(side="top", pady=10, fill="x", anchor="w")
    return top_frame

def create_csv_frame(top_frame):
    csv_frame = tk.Frame(top_frame)
    csv_frame.pack(pady=5, fill="x", anchor="w")
    return csv_frame

def create_load_button(csv_frame):
    def load_file_and_print_result():
        file_name = handle_load_file()
        if file_name is not None:
            csv_path_label.config(text=f"Loaded file: {file_name}")
            enable_buttons()  # Enable buttons after successful file load
        return

    load_button = tk.Button(csv_frame, text="Load File", command=load_file_and_print_result)
    load_button.pack(side="left", padx=5, anchor="w")
    return load_button

def create_csv_path_label(csv_frame):
    csv_path_label = tk.Label(csv_frame, text="Loaded file: None", font=("Arial", 10), anchor="w")
    csv_path_label.pack(side="left", padx=5, fill="x", expand=True, anchor="w")
    return csv_path_label

def create_result_button_frame(top_frame):
    result_button_frame = tk.Frame(top_frame)
    result_button_frame.pack(pady=5, fill="x", anchor="w")
    return result_button_frame

def create_parse_button(result_button_frame):
    parse_button = tk.Button(result_button_frame, text="Show Results", command=show_result)
    parse_button.pack(side="left", padx=5, anchor="w")
    return parse_button

def create_expand_collapse_button(result_button_frame):
    def toggle_json_tree_expand_collapse():
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

    expand_collapse_button = tk.Button(result_button_frame, text="Expand/Collapse", command=toggle_json_tree_expand_collapse)
    expand_collapse_button.pack(side="left", padx=5, anchor="w")
    return expand_collapse_button

def create_radio_frame(result_button_frame):
    radio_frame = tk.Frame(result_button_frame)
    radio_frame.pack(side="left", pady=5, anchor="w")
    return radio_frame

def create_pf_radio_buttons(radio_frame):
    pf_var = tk.IntVar(value=1)
    set_selected_pf(PLATFORM_LABELS[pf_var.get()])
    for index, option in enumerate(PLATFORM_LABELS):
        tk.Radiobutton(radio_frame, text=option, variable=pf_var, value=index, anchor="w").pack(side="left", anchor="w")
    pf_var.trace_add("write", lambda *args: (set_selected_pf(PLATFORM_LABELS[pf_var.get()]), print(f"selected_pf: {get_selected_pf()}")))
    return pf_var

def create_left_frame(main_frame):
    left_frame = tk.Frame(main_frame)
    left_frame.pack(side="left", padx=10, anchor="nw")
    return left_frame

def create_date_dropdowns(left_frame):
    tk.Label(left_frame, text="Start Date (datetime):", font=("Arial", 10), anchor="w").pack(side="top", anchor="w")
    start_date_var = tk.StringVar(value=None)
    start_date_dropdown = ttk.Combobox(left_frame, textvariable=start_date_var, state="readonly")
    start_date_dropdown.pack(pady=5, side="top", anchor="w")

    tk.Label(left_frame, text="End Date (datetime):", font=("Arial", 10), anchor="w").pack(side="top", anchor="w")
    end_date_var = tk.StringVar(value=None)
    end_date_dropdown = ttk.Combobox(left_frame, textvariable=end_date_var, state="readonly")
    end_date_dropdown.pack(pady=5, side="top", anchor="w")

    return start_date_var, end_date_var, start_date_dropdown, end_date_dropdown

def get_start_date_var():
    return start_date_var.get()

def get_end_date_var():
    return end_date_var.get()

def create_url_filter(left_frame):
    tk.Label(left_frame, text="URL Filter:", font=("Arial", 10), anchor="w").pack(side="top", anchor="w")
    url_var = tk.IntVar(value=0)
    for index, option in enumerate(URL_LABELS):
        tk.Radiobutton(left_frame, text=option, variable=url_var, value=index, anchor="w").pack(side="top", anchor="w")
    url_var.trace_add("write", update_visibility)
    return url_var

def get_url_var():
    return url_var.get()

def create_req_body_filter(left_frame):
    reqbody_label = tk.Label(left_frame, text="ReqBody Filter:", font=("Arial", 10), anchor="w")
    reqbody_label.pack(side="top", anchor="w")
    reqbody_entry = tk.Entry(left_frame)
    return reqbody_label, reqbody_entry

def get_reqbody_entry():
    return reqbody_entry.get()

def create_res_body_filter(left_frame):
    resbody_label = tk.Label(left_frame, text="ResBody Filter:", font=("Arial", 10), anchor="w")
    resbody_label.pack(side="top", anchor="w")
    resbody_entry = tk.Entry(left_frame)
    return resbody_label, resbody_entry

def get_resbody_entry():
    return resbody_entry.get()

def create_service_flag_checkboxes(left_frame):
    service_flag_label = tk.Label(left_frame, text="Options:", anchor="w", font=("Arial", 10))
    service_flag_label.pack(side="top", anchor="w")
    service_flag_checkbox_frame = tk.Frame(left_frame)
    service_flag_checkbox_frame.pack(side="top", anchor="w")
    service_flag_checkbox_vars = []
    service_flag_checkboxes = []
    for label in SERVICE_FLAG_LABELS:
        var = tk.BooleanVar(value=(label in ["Telematics"]))
        service_flag_checkbox_vars.append(var)
        checkbox = tk.Checkbutton(service_flag_checkbox_frame, text=label, variable=var)
        checkbox.pack(anchor="w")
        service_flag_checkboxes.append(checkbox)
    return service_flag_label, service_flag_checkbox_frame, service_flag_checkbox_vars, service_flag_checkboxes

def get_service_flag_checkbox_vars():
    return service_flag_checkbox_vars

def create_remote_control_checkboxes(left_frame):
    remote_control_label = tk.Label(left_frame, text="Options:", anchor="w", font=("Arial", 10))
    remote_control_label.pack(side="top", anchor="w")
    remote_control_vars = []
    remote_checkboxes = []
    for label in REMOTE_CONTROL_LABELS:
        var = tk.BooleanVar(value=False)
        remote_control_vars.append(var)
        checkbox = tk.Checkbutton(left_frame, text=label, variable=var)
        checkbox.pack(anchor="w")
        remote_checkboxes.append(checkbox)
    return remote_control_label, remote_control_vars, remote_checkboxes

def get_remote_control_vars():
    return remote_control_vars

def create_service_category_dropdown(left_frame):
    service_category_label = tk.Label(left_frame, text="Service Category Filter:", anchor="w", font=("Arial", 10))
    service_category_var = tk.StringVar()
    service_category_keys = list(SERVICE_TYPE_TABLE.keys())
    service_category_values = list(SERVICE_TYPE_TABLE.values())
    if service_category_keys:
        service_category_var.set(f"({service_category_keys[0]}) {service_category_values[0]}")
    service_category_dropdown = tk.OptionMenu(left_frame, service_category_var, *[f"({key}) {value}" for key, value in SERVICE_TYPE_TABLE.items()])
    service_category_var.trace_add("write", lambda *args: (set_selected_service_category(service_category_var.get().split(")")[0].strip("(")), print(f"Selected Service Category Key: {service_category_var.get().split(')')[0].strip('(')}")))
    return service_category_label, service_category_var, service_category_dropdown

def get_service_category_var():
    return service_category_var.get()

def create_right_frame(main_frame):
    right_frame = tk.Frame(main_frame)
    right_frame.pack(side="right", padx=10, fill="both", expand="true", anchor="nw")
    return right_frame

def create_json_treeview(right_frame):
    result_label = tk.Label(right_frame, text="Console:", font=("Arial", 10, "bold"))
    result_label.pack(anchor="nw")
    result_frame = tk.Frame(right_frame)
    result_frame.pack(fill="both", expand="true", anchor="nw")
    json_tree = ttk.Treeview(result_frame)
    json_tree_scroll_y = tk.Scrollbar(result_frame, orient="vertical", command=json_tree.yview)
    json_tree_scroll_x = tk.Scrollbar(result_frame, orient="horizontal", command=json_tree.xview)
    json_tree.configure(yscrollcommand=json_tree_scroll_y.set, xscrollcommand=json_tree_scroll_x.set)
    json_tree.grid(row=0, column=0, sticky="nsew")
    json_tree_scroll_y.grid(row=0, column=1, sticky="ns")
    json_tree_scroll_x.grid(row=1, column=0, sticky="ew")
    result_frame.grid_rowconfigure(0, weight=1)
    result_frame.grid_columnconfigure(0, weight=1)
    json_tree["columns"] = ("Value",)
    json_tree.column("#0", minwidth=150, width=500, stretch=True, anchor="w")
    json_tree.column("Value", minwidth=150, width=500, stretch=True, anchor="w")
    json_tree.heading("#0", text="Key", anchor="w")
    json_tree.heading("Value", text="Value", anchor="w")
    return json_tree

def get_json_tree():
    return json_tree

# Increase the size of the result frame by 30%
# root.update_idletasks()  # Ensure the window is fully rendered before resizing
# result_frame.config(width=int(root.winfo_width() * 0.7), height=int(root.winfo_height() * 0.7))

# Add columns to the Treeview
# json_tree.config(height=30)

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

# Disable buttons initially
def disable_buttons():
    parse_button.config(state="disabled")
    expand_collapse_button.config(state="disabled")

def enable_buttons():
    parse_button.config(state="normal")
    expand_collapse_button.config(state="normal")

def initialize_gui():
    global root, main_frame, top_frame, csv_frame, load_button, csv_path_label, result_button_frame, parse_button, expand_collapse_button
    global radio_frame, pf_var, left_frame, start_date_var, end_date_var, start_date_dropdown, end_date_dropdown, url_var
    global reqbody_label, reqbody_entry, resbody_label, resbody_entry, service_flag_label, service_flag_checkbox_frame
    global service_flag_checkbox_vars, service_flag_checkboxes, remote_control_label, remote_control_vars, remote_checkboxes
    global service_category_label, service_category_var, service_category_dropdown, right_frame, json_tree

    root = create_root_window()
    main_frame = create_main_frame(root)
    top_frame = create_top_frame(main_frame)
    csv_frame = create_csv_frame(top_frame)
    load_button = create_load_button(csv_frame)
    csv_path_label = create_csv_path_label(csv_frame)
    result_button_frame = create_result_button_frame(top_frame)
    parse_button = create_parse_button(result_button_frame)
    expand_collapse_button = create_expand_collapse_button(result_button_frame)
    radio_frame = create_radio_frame(result_button_frame)
    pf_var = create_pf_radio_buttons(radio_frame)
    left_frame = create_left_frame(main_frame)
    start_date_var, end_date_var, start_date_dropdown, end_date_dropdown = create_date_dropdowns(left_frame)
    url_var = create_url_filter(left_frame)
    reqbody_label, reqbody_entry = create_req_body_filter(left_frame)
    resbody_label, resbody_entry = create_res_body_filter(left_frame)
    service_flag_label, service_flag_checkbox_frame, service_flag_checkbox_vars, service_flag_checkboxes = create_service_flag_checkboxes(left_frame)
    remote_control_label, remote_control_vars, remote_checkboxes = create_remote_control_checkboxes(left_frame)
    service_category_label, service_category_var, service_category_dropdown = create_service_category_dropdown(left_frame)
    right_frame = create_right_frame(main_frame)
    json_tree = create_json_treeview(right_frame)

    disable_buttons()
    update_visibility()
    root.mainloop()

initialize_gui()
