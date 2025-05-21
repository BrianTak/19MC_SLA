import pandas as pd
import tkinter as tk

from remote_control.remote_control_resrmtctrl import (
    parse_resrmtctrl_header,
    parse_resrmtctrl_body
)

from remote_control.remote_control_rmtctrlcmd import (
    parse_rmtctrlcmd_header,
    parse_rmtctrlcmd_body
)

from util.config import (
    REMOTE_CONTROL_CMD_URL,
    REMOTE_CONTROL_RESP_URL,
    get_selected_service_category
)

from util.database import (
    get_filtered_data
)

def should_skip_entry(service_type, service_category):
    """
    Determines whether an entry should be skipped based on the selected type and service category.

    Args:
        selected_type (str): The type to check against.
        service_category (str): The service category to compare.

    Returns:
        bool: True if the entry should be skipped, False otherwise.
    """
    return service_type != service_category and service_category != "00"

def process_remote_control():
    """
    Checks remote control commands in the filtered data for two specific URLs and returns the results.

    Returns:
        pd.DataFrame: A DataFrame containing the results of the remote control check.
    """

    result = []

    print("Starting remote control check.")
    print(f"Filtered data:\n{get_filtered_data()}")

    for index, row in get_filtered_data().iterrows():
        if row['url'] == REMOTE_CONTROL_CMD_URL and 'resbody' in row and pd.notna(row['resbody']):
            # Parse header and body data
            header_data = parse_rmtctrlcmd_header(row['resbody'])
            body_data = parse_rmtctrlcmd_body(row['resbody'])

            # Iterate through options in body_data
            options = body_data.get("Option", [])
            skip_entry = True  # Initialize as True
            for option in options:
                service_type = option.get("Service Type", "N/A").split(":")[0]
                service_category = get_selected_service_category()
                if not should_skip_entry(service_type, service_category):
                    skip_entry = False  # If any option should not be skipped, set skip_entry to False
                    break

            if skip_entry:
                # print(f"[DEBUG] Skipping entry with Service Type: {service_type} != selected category: {service_category}")
                continue

            result.append({
                'Datetime': row['datetime'],
                'URL': REMOTE_CONTROL_CMD_URL,
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

            skip_entry = True  # Initialize as True
            options = body_data.get("Operation Results", [])
            for option in options:
                service_type_1 = option.get("Center Request Command", {}).get("Service Type", "N/A").split(":")[0]
                service_type_2 = option.get("Operation Result Command", {}).get("Service Type", "N/A").split(":")[0]
                service_category = get_selected_service_category()
                if not should_skip_entry(service_type_1, service_category) or not should_skip_entry(service_type_2, service_category):
                    skip_entry = False  # If any command should not be skipped, set skip_entry to False
                    break

            if skip_entry:
                # print(f"[DEBUG] Skipping entry with Service Type 1: {service_type_1} or Service Type 2: {service_type_2} != selected category: {service_category}")
                continue

            # Add parsed data to the result
            result.append({
                'Datetime': row['datetime'],
                'URL': REMOTE_CONTROL_RESP_URL,
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