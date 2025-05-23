# Renamed to `service_flag_tracker.py` for clarity
import xml.etree.ElementTree as ET
import pandas as pd

from util.config import (
    get_selected_service_flags
)
from util.database import (
    get_filtered_data
)

def process_service_flags():
    """
    Processes the filtered data for service flag checking, grouping by date and combining checkbox selections.

    Args:
        filtered_data (pd.DataFrame): The filtered DataFrame.
        checkbox_vars (list): List of checkbox variables.
        checkbox_labels (list): List of checkbox labels.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    result = []
    for _, row in get_filtered_data().iterrows():
        try:
            source = "resbody" if 'resbody' in row and pd.notna(row['resbody']) else "reqbody"
            xml_content = row[source]
            root = ET.fromstring(xml_content)
            for srvset in root.findall(".//SrvSet"):
                srv_type = srvset.get('type', 'N/A')
                srv_result = srvset.text if srvset.text else 'N/A'

                url_name = "srvflg" if "srvflg" in row['url'] else "rscdlchk"

                if srv_type in get_selected_service_flags():
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

    return pd.DataFrame(result)

