# Renamed to `service_flag_tracker.py` for clarity
import xml.etree.ElementTree as ET
import pandas as pd
import tkinter as tk

# URL Constants
SERVICE_FLAG_URL = "http://dcmservice-provisioning-service.local/mc/telematics/srvflg/"
RSCDLCHK_URL = "http://dcmservice-provisioning-service.local/mc/telematics/rscdlchk/"

# Checkbox Labels
CHECKBOX_LABELS = ["Telematics", "RSFlag", "RmtCtrl", "SVT", "VPPlus", "VP", "Alarm", "RmtImmobi", "RmtConf", "Dormant"]

def process_service_flags(filtered_data, checkbox_vars, checkbox_labels):
    """
    Processes the filtered data for service flag checking, grouping by date and combining checkbox selections.

    Args:
        filtered_data (pd.DataFrame): The filtered DataFrame.
        checkbox_vars (list): List of checkbox variables.
        checkbox_labels (list): List of checkbox labels.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    selected_checkboxes = [
        label for var, label in zip(checkbox_vars, checkbox_labels) if var.get()
    ]

    filtered_data = filtered_data[
        filtered_data['url'].isin([SERVICE_FLAG_URL, RSCDLCHK_URL])
    ]

    filtered_data = filtered_data.copy()  # Avoid SettingWithCopyWarning
    filtered_data.columns = filtered_data.columns.str.strip().str.lower()
    filtered_data['url'] = filtered_data['url'].str.strip().str.lower()

    if 'url' not in filtered_data.columns or 'resbody' not in filtered_data.columns:
        print("[ERROR] Required columns are missing in the data.")
        return pd.DataFrame()

    result = []
    for _, row in filtered_data.iterrows():
        try:
            source = "resbody" if 'resbody' in row and pd.notna(row['resbody']) else "reqbody"
            xml_content = row[source]
            root = ET.fromstring(xml_content)
            for srvset in root.findall(".//SrvSet"):
                srv_type = srvset.get('type', 'N/A')
                srv_result = srvset.text if srvset.text else 'N/A'

                url_name = "srvflg" if row['url'] == SERVICE_FLAG_URL else "rscdlchk"

                if srv_type in selected_checkboxes:
                    result.append({
                        'Datetime': row['datetime'],  # Group by date
                        'URL': url_name,
                        'Source': source,
                        'Result': {srv_type: srv_result}
                    })
        except ET.ParseError as e:
            result.append({
                'Datetime': row['datetime'],
                'URL': 'ParseError',
                'Source': source if 'source' in locals() else 'Unknown',
                'Result': str(e)
            })

    # Convert to DataFrame and group by date
    result_df = pd.DataFrame(result)
    if not result_df.empty:
        grouped = result_df.groupby('Datetime').agg({
            'URL': 'first',  # Keep the first URL for simplicity
            'Source': 'first',  # Keep the first source for simplicity
            'Result': lambda x: {k: v for d in x for k, v in d.items() if isinstance(d, dict)},
        }).reset_index()

        return grouped

    return pd.DataFrame()

def create_service_flag_checkboxes(parent_frame):
    """
    Creates checkboxes for service flag options, with Telematics and RSFlag checked by default.

    Args:
        parent_frame (tk.Frame): The parent frame where the checkboxes will be added.

    Returns:
        tuple: (checkbox_vars, checkbox_labels, checkbox_frame, checkboxes)
    """
    checkbox_frame = tk.Frame(parent_frame)
    checkbox_vars = [tk.BooleanVar(value=(label in ["Telematics", "RSFlag"])) for label in CHECKBOX_LABELS]
    checkboxes = []

    for i, label in enumerate(CHECKBOX_LABELS):
        cb = tk.Checkbutton(checkbox_frame, text=label, variable=checkbox_vars[i])
        checkboxes.append(cb)

    return checkbox_vars, CHECKBOX_LABELS, checkbox_frame, checkboxes