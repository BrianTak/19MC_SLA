
def create_url_filter(left_frame, url_var, url_options):
    """Create URL filter radio buttons."""
    tk.Label(left_frame, text="URL Filter:", font=("Arial", 10), anchor="w").pack(side="top", anchor="w")
    for index, option in enumerate(url_options):
        tk.Radiobutton(left_frame, text=option, variable=url_var, value=index, anchor="w").pack(side="top", anchor="w")


def create_reqbody_filter(left_frame):
    """Create ReqBody filter entry."""
    reqbody_label = tk.Label(left_frame, text="ReqBody Filter:", font=("Arial", 10), anchor="w")
    reqbody_entry = tk.Entry(left_frame)
    reqbody_label.pack_forget()  # Hidden by default
    reqbody_entry.pack_forget()  # Hidden by default
    return reqbody_label, reqbody_entry


def create_resbody_filter(left_frame):
    """Create ResBody filter entry."""
    resbody_label = tk.Label(left_frame, text="ResBody Filter:", font=("Arial", 10), anchor="w")
    resbody_entry = tk.Entry(left_frame)
    resbody_label.pack_forget()  # Hidden by default
    resbody_entry.pack_forget()  # Hidden by default
    return resbody_label, resbody_entry


def create_service_flag_checkboxes(left_frame, checkbox_labels):
    """Create Service Flag checkboxes."""
    service_flag_label = tk.Label(left_frame, text="Options:", anchor="w", font=("Arial", 10))
    service_flag_checkbox_frame = tk.Frame(left_frame)
    service_flag_checkbox_vars = []
    service_flag_checkboxes = []

    for label in checkbox_labels:
        var = tk.BooleanVar(value=(label in ["Telematics"]))  # Default check for Telematics
        service_flag_checkbox_vars.append(var)
        cb = tk.Checkbutton(service_flag_checkbox_frame, text=label, variable=var)
        service_flag_checkboxes.append(cb)

    service_flag_checkbox_frame.pack(pady=5, side="top", anchor="w")
    service_flag_checkbox_frame.pack_forget()  # Hidden by default
    service_flag_label.pack(side="top", anchor="w")
    service_flag_label.pack_forget()  # Hidden by default

    return service_flag_label, service_flag_checkbox_frame, service_flag_checkbox_vars, service_flag_checkboxes


def create_remote_control_checkboxes(left_frame, remote_checkbox_labels):
    """Create Remote Control checkboxes."""
    remote_control_label = tk.Label(left_frame, text="Options:", anchor="w", font=("Arial", 10))
    remote_checkbox_vars = []
    remote_checkboxes = []

    for label in remote_checkbox_labels:
        var = tk.BooleanVar(value=False)
        remote_checkbox_vars.append(var)
        checkbox = tk.Checkbutton(left_frame, text=label, variable=var)
        remote_checkboxes.append(checkbox)
        checkbox.pack(anchor="w")
        checkbox.pack_forget()  # Initially hidden

    remote_control_label.pack(side="top", anchor="w")
    remote_control_label.pack_forget()  # Initially hidden

    return remote_control_label, remote_checkbox_vars, remote_checkboxes


def create_service_category_dropdown(left_frame, service_type_table):
    """Create Service Category dropdown."""
    service_category_var = tk.StringVar()
    service_category_keys = list(service_type_table.keys())
    service_category_values = list(service_type_table.values())

    if service_category_keys:
        service_category_var.set(f"({service_category_keys[0]}) {service_category_values[0]}")

    service_category_dropdown = tk.OptionMenu(
        left_frame, service_category_var, *[f"({key}) {value}" for key, value in service_type_table.items()]
    )
    service_category_dropdown.pack_forget()  # Initially hidden

    service_category_label = tk.Label(left_frame, text="Service Category Filter:", anchor="w", font=("Arial", 10))
    service_category_label.pack_forget()  # Initially hidden

    return service_category_label, service_category_dropdown, service_category_var


def create_json_tree(result_frame):
    """Create JSON Treeview with scrollbars."""
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
    json_tree.config(height=30)

    return json_tree


def update_visibility(
    url_var,
    json_tree,
    reqbody_label,
    reqbody_entry,
    resbody_label,
    resbody_entry,
    service_flag_label,
    service_flag_checkbox_frame,
    service_flag_checkboxes,
    remote_control_label,
    remote_checkboxes,
    service_category_label,
    service_category_dropdown,
):
    """Update visibility of UI elements based on URL filter selection."""
    for item in json_tree.get_children():
        json_tree.delete(item)

    if url_var.get() == 0:  # "Service Flag Checker" is selected
        reqbody_label.pack_forget()
        reqbody_entry.pack_forget()
        resbody_label.pack_forget()
        resbody_entry.pack_forget()
        service_flag_label.pack(anchor="w")
        service_flag_checkbox_frame.pack(pady=5, anchor="w")
        for cb in service_flag_checkboxes:
            cb.pack(anchor="w")
        remote_control_label.pack_forget()
        for cb in remote_checkboxes:
            cb.pack_forget()
        service_category_label.pack_forget()
        service_category_dropdown.pack_forget()
    elif url_var.get() == 1:  # "Remote Control Checker" is selected
        reqbody_label.pack_forget()
        reqbody_entry.pack_forget()
        resbody_label.pack_forget()
        resbody_entry.pack_forget()
        service_flag_label.pack_forget()
        service_flag_checkbox_frame.pack_forget()
        for cb in service_flag_checkboxes:
            cb.pack_forget()
        remote_control_label.pack(anchor="w")
        for cb in remote_checkboxes:
            cb.pack(anchor="w")
        service_category_label.pack(anchor="w")
        service_category_dropdown.pack(anchor="w")
    else:
        reqbody_label.pack(anchor="w")
        reqbody_entry.pack(pady=5, anchor="w")
        resbody_label.pack(anchor="w")
        resbody_entry.pack(pady=5, anchor="w")
        service_flag_label.pack_forget()
        service_flag_checkbox_frame.pack_forget()
        for cb in service_flag_checkboxes:
            cb.pack_forget()
        remote_control_label.pack_forget()
        for cb in remote_checkboxes:
            cb.pack_forget()
        service_category_label.pack_forget()
        service_category_dropdown.pack_forget()
