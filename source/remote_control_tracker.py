import pandas as pd
import tkinter as tk

from remote_control_resrmtctrl import (
    parse_resrmtctrl_header,
    parse_resrmtctrl_body
)

from remote_control_rmtctrlcmd import (
    parse_rmtctrlcmd_header,
    parse_rmtctrlcmd_body
)

REMOTE_CONTROL_CMD_URL = "http://dcmservice-remocon-service.local/remoteservices/rmtctrlcmd/"
REMOTE_CONTROL_RESP_URL = "http://dcmservice-remocon-service.local/mc/remoteservices/resrmtctrl/"

URL_NAME_MAPPING = {
    REMOTE_CONTROL_CMD_URL: "rmtctrlcmd",
    REMOTE_CONTROL_RESP_URL: "resrmtctrl"
}

def create_remote_control_checkboxes(parent_frame):
    """
    Creates checkboxes for remote control options.

    Args:
        parent_frame: The parent frame where the checkboxes will be added.

    Returns:
        tuple: A tuple containing the checkbox variables and labels.
    """
    checkbox_vars = []
    checkbox_labels = ["rmtctrlcmd", "resrmtctrl"]
    checkboxes = []

    for label in checkbox_labels:
        var = tk.BooleanVar(value=False)
        checkbox_vars.append(var)
        checkbox = tk.Checkbutton(parent_frame, text=label, variable=var)
        checkboxes.append(checkbox)
        checkbox.pack(anchor="w")

    return checkbox_vars, checkbox_labels, checkboxes

def process_remote_control(filtered_data, checkbox_vars, checkbox_labels):
    """
    Checks remote control commands in the filtered data for two specific URLs and returns the results.

    Args:
        filtered_data (pd.DataFrame): The filtered DataFrame containing the data to check.
        checkbox_vars (list): List of checkbox variables.
        checkbox_labels (list): List of checkbox labels.

    Returns:
        pd.DataFrame: A DataFrame containing the results of the remote control check.
    """
    # Determine selected checkboxes
    selected_urls = []
    if any(var.get() for var, label in zip(checkbox_vars, checkbox_labels) if label == "rmtctrlcmd"):
        selected_urls.append(REMOTE_CONTROL_CMD_URL)
    if any(var.get() for var, label in zip(checkbox_vars, checkbox_labels) if label == "resrmtctrl"):
        selected_urls.append(REMOTE_CONTROL_RESP_URL)

    # If no specific URLs are selected, include all
    if not selected_urls:
        selected_urls = [REMOTE_CONTROL_CMD_URL, REMOTE_CONTROL_RESP_URL]

    # Filter data based on selected URLs
    if selected_urls:
        filtered_data = filtered_data[filtered_data['url'].isin(selected_urls)]

    # Ensure column names are standardized
    filtered_data.columns = filtered_data.columns.str.strip().str.lower()
    filtered_data['url'] = filtered_data['url'].str.strip().str.lower()

    result = []
    print("Starting remote control check.")
    print(f"Filtered data:\n{filtered_data}")

    for index, row in filtered_data.iterrows():
        urlname = URL_NAME_MAPPING.get(row['url'], "unknown_service")

        if row['url'] == REMOTE_CONTROL_CMD_URL and 'resbody' in row and pd.notna(row['resbody']):
            # Parse header and body data
            header_data = parse_rmtctrlcmd_header(row['resbody'])
            body_data = parse_rmtctrlcmd_body(row['resbody'])

            if "Filtered" in body_data:
                print(f"[DEBUG] Filtered by: {body_data['Filtered']}")
                continue  # Skip this entry if filtered by service category

            # Add parsed data to the result
            result.append({
                'Datetime': row['datetime'],
                'URL': urlname,
                'Source': 'resbody',
                "Protocol Version": header_data.get("Protocol Version", "N/A"),
                "Message ID": header_data.get("Message ID", "N/A"),
                "Request ID": header_data.get("Request ID", "N/A"),
                'Request Date': header_data.get("Request Date", "N/A"),
                'Option Count': body_data.get("Option Count", "N/A"),
                'Option': body_data.get("Option", "N/A"),
            })

        elif row['url'] == REMOTE_CONTROL_RESP_URL and 'reqbody' in row and pd.notna(row['reqbody']):
            # Parse header and body data
            header_data = parse_resrmtctrl_header(row['reqbody'])
            body_data = parse_resrmtctrl_body(row['reqbody'])

            if "Filtered" in body_data:
                print(f"[DEBUG] Filtered by: {body_data['Filtered']}")
                continue  # Skip this entry if filtered by service category

            # Add parsed data to the result
            result.append({
                'Datetime': row['datetime'],
                'URL': urlname,
                'Source': 'reqbody',
                'ReqFilename': row.get('reqfilename', 'N/A'),  # Add reqfilename field
                'Status': header_data.get('Status', 'N/A'),
                'DCM Number': header_data.get('DCM Number', 'N/A'),
                "BSID": header_data.get('BSID', 'N/A'),
                "SID": header_data.get('SID', 'N/A'),
                "NID": header_data.get('NID', 'N/A'),
                'Time of Dormant': header_data.get('Time of Dormant', 'N/A'),
                'Position Info Category': body_data.get('Position Info Category', 'N/A'),
                "Position Info": body_data.get('Position Info', 'N/A'),
                'Body Info Length': body_data.get('Body Info Length', 'N/A'),
                "Table Version": body_data.get('Table Version', []),
                "Pre-operation Vehicle State": body_data.get('Pre-operation Vehicle State', []),
                "Time Infomation": body_data.get('Time Infomation', []),
                "Operation Results": body_data.get('Operation Results', []),
                "Vehicle State when Remote A/C": body_data.get('Vehicle State when Remote A/C', [])
            })

    print("Remote control check completed.")
    return pd.DataFrame(result)