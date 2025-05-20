from config import get_selected_pf  # Import selected_pf from config

from remote_control_common import (
    parse_time_information,
    parse_option
)

from remote_control_map import (
    PRE_OPERATION_VEHICLE_TABLE,
    VEHICLE_STATE_WHEN_REMOTE_AC,
    CANCEL_PERMISSION_STATES
)

def parse_cancel_permission_states(data):
    """
    Parses the Cancel Permission data.

    Args:
        data (str): The raw data as a hexadecimal string.

    Returns:
        dict: A dictionary containing the parsed cancel permission states.
    """
    try:
        if len(data) != 2:  # 1 byte = 2 hex characters
            return {"Error": "Invalid Cancel Permission length"}

        cancel_permission_states = {
            "Hazard Lamps OFF Cancel Permission State": data[0],
            "Lock Cancel Permission State": data[1],
            "PW Close Cancel Permission State": data[2]
        }

        return cancel_permission_states

    except Exception as e:
        return {"Error": f"Cancel Permission parsing error: {e}"}

def parse_operation_results_15PF(header_code, data):
     try:
        # Ensure the data is long enough to parse
        if len(data) < 12:  # Minimum length required for one operation result (6 bytes * 2)
            return {"Error": "Operation Results data too short"}

        # # Parse Center Request Command (3 bytes)
        # center_request_command = data[:6]  # 3 bytes = 6 hex chars
        # center_request_command_parsed = parse_option(center_request_command)

        # # Parse Operation Command (1 byte)
        # operation_command = data[6:8]  # 1 byte = 2 hex chars

        # # Parse Operation Parameter (1 byte)
        # operation_parameter = data[8:10]  # 1 byte = 2 hex chars

        # # Parse Result (1 byte)
        # result = data[10:12]  # 1 byte = 2 hex chars

        # # Parse Result Parameter 1 (1 byte)
        # result_parameter_1 = data[12:14]  # 1 byte = 2 hex chars

        # # Parse Result Parameter 2 (1 byte)
        # result_parameter_2 = data[14:16]  # 1 byte = 2 hex chars

        # # Combine parsed data into a dictionary
        # center_request_command_parsed.update({
        #     "Operation Command": operation_command,
        #     "Operation Parameter": operation_parameter,
        #     "Result": result,
        #     "Result Parameter 1": result_parameter_1,
        #     "Result Parameter 2": result_parameter_2
        # })


        return {}

     except Exception as e:
        return {"Error": f"Parsing error: {e}"}

def parse_operation_results_19PF(data):
    """
    Parses the Operation Results from the given data.

    Args:
        data (str): The raw data as a hexadecimal string.

    Returns:
        dict: A dictionary containing the parsed operation results.
    """
    try:
        # Ensure the data is long enough to parse
        if len(data) < 28:  # Minimum length required for one operation result (14 bytes * 2)
            return {"Error": "Operation Results data too short"}

        # Parse Center Request Command (7 bytes)
        center_request_command = data[:14]  # 7 bytes = 14 hex chars
        center_request_command_parsed = parse_option(center_request_command)

        # Parse Operation Result Command (7 bytes)
        operation_result_command = data[14:28]  # 7 bytes = 14 hex chars
        operation_result_command_parsed = parse_option(operation_result_command)

        if "Filtered" in center_request_command_parsed or "Filtered" in operation_result_command_parsed:
            return {"Filtered": "service category"}

        combined_result = {
            "Center Request Command": center_request_command_parsed,
            "Operation Result Command": operation_result_command_parsed
        }

        return combined_result

    except Exception as e:
        return {"Error": f"Parsing error: {e}"}

# Header parsing function
# Parses the header of the reqbody data for resrmtctrl.
def parse_resrmtctrl_header(reqbody):
    """
    Parses the header of the reqbody data for resrmtctrl.

    Args:
        reqbody (str): The raw reqbody data as a string.

    Returns:
        dict: A dictionary containing the parsed header fields.
    """
    try:
        # Ensure the data is long enough to parse the header
        if len(reqbody) < 34:  # Minimum length required for the header
            return {"Error": "Header data too short"}

        # Parse header fields
        status = reqbody[:2]  # 1 byte (2 hex characters)
        dcm_number = reqbody[2:18]  # 8 bytes (16 hex characters)
        bsid = reqbody[18:22]  # 2 bytes (4 hex characters)
        sid = reqbody[22:26]  # 2 bytes (4 hex characters)
        nid = reqbody[26:30]  # 2 bytes (4 hex characters)

        # Convert time_of_day to a human-readable format (2 bytes per field)
        time_of_day = reqbody[30:54]  # 12 bytes (24 hex characters)
        time_of_day_formatted = parse_time_information(time_of_day).get("Time", "N/A")

        # Return parsed header fields
        return {
            "Status": status,
            "DCM Number": dcm_number,
            "BSID": bsid,
            "SID": sid,
            "NID": nid,
            "Time of Dormant": time_of_day_formatted
        }

    except Exception as e:
        return {"Error": f"Header parsing error: {e}"}

# Body parsing function
# Parses the body of the reqbody data for resrmtctrl.
def parse_resrmtctrl_body(reqbody):
    """
    Parses the body of the reqbody data for resrmtctrl.

    Args:
        reqbody (str): The raw reqbody data as a string.

    Returns:
        dict: A dictionary containing the parsed body fields.
    """
    try:
        table_version_result = {}
        pre_operation_result = {}
        time_information_result = {}
        cancel_permission_states_result = {}
        operation_result = {}
        vehicle_state_result = {}

        # Parse Position Info Category (1 byte)
        position_info_category = reqbody[54:56]  # 1 byte (2 hex characters)

        # Parse Position Info
        position_info = reqbody[56:108]

        # Parse Body Info Length (4 bytes)
        try:
            body_info_length = int(reqbody[108:116], 16) * 2
        except ValueError as e:
            print(f"[DEBUG] Error parsing body_info_length: {e}")
            return {"Error": "Invalid Body Info Length"}

        # Parse Message Category (1 byte)
        message_category = reqbody[116:118]  # 1 byte (2 hex characters)

        # Parse Body Info
        body_info = reqbody[118:118 + body_info_length]  # 0 to 200 bytes

        # Process Body Info sequentially
        offset = 0
        while offset < len(body_info):
            header_code = body_info[offset:offset + 2].upper()  # Read the header code (1 byte) and convert to uppercase
            offset += 2  # Skip the header code

            if header_code == "F0":  # Table Version
                data_length = 1  # Table Version is 1 bytes
                table_version_data = body_info[offset:offset + data_length * 2]
                table_version_result.setdefault("Table Version", []).append(
                    {"Major Version": int(table_version_data[0], 16),
                     "Minor Version": int(table_version_data[1], 16)}
                )
                offset += data_length * 2

            elif header_code in ["01", "10", "11", "12", "13", "20", "21", "22", "23", "24", "25"]:  # Pre-operation Vehicle State
                data_length = 1  # Each of Pre-operation Vehicle State is 2 bytes
                pre_operation_data = body_info[offset:offset + data_length * 2]
                pre_operation_result.setdefault("Pre-operation Vehicle State", []).append(
                    PRE_OPERATION_VEHICLE_TABLE.get(header_code, lambda _: "Unknown")(pre_operation_data)
                )
                offset += data_length * 2

            elif header_code in ["80", "81", "82", "83"]:  # Time Information
                data_length = 12  # Time Information is 12 bytes
                time_data = body_info[offset:offset + data_length * 2]
                labels = ["Center Time Stamp", "Request Reception Time", "Operation End Time", "Standby Start Time"]
                label_index = int(header_code, 16) - 0x80
                time_information_result.setdefault("Time Information", []).append(
                    {labels[label_index]: parse_time_information(time_data).get("Time", "N/A")}
                )
                offset += data_length * 2

            elif header_code in ["A0"]:
                if get_selected_pf() in ["15PF"]:
                    data_length = 2  # Cancel permission state is 2 bytes
                    cancel_permission_data = body_info[offset:offset + data_length * 2]
                    cancel_permission_states_result.setdefault("Cancel Permission States", []).append(
                            CANCEL_PERMISSION_STATES.get(header_code, lambda _: "Unknown")(cancel_permission_data)
                        )
                    offset += data_length * 2
                else:
                    print(f"[DEBUG] Unknown header code: {header_code}, selected_pf: {get_selected_pf()}")
                    break

            elif header_code in ["C0", "C1", "C2", "C4", "C5", "EF"]:  # Operation Results
                if get_selected_pf() in ["15PF"]:
                    data_length = 6
                    operation_data = body_info[offset:offset + data_length * 2]
                    parsed_result = parse_operation_results_15PF(operation_data)
                    if "Filtered" in parsed_result:
                        return {"Filtered": "service category"}
                    else:
                        operation_result.setdefault("Operation Results", []).append(parsed_result)
                        offset += data_length * 2
                else:
                    print(f"[DEBUG] Unknown header code: {header_code}, selected_pf: {get_selected_pf()}")
                    break

            elif header_code in ["D1", "D2", "D3", "D4", "D5", "D6", "D7"]:  # Operation Results
                if get_selected_pf() in ["19PF", "19PFv2"]:
                    data_length = 14
                    operation_data = body_info[offset:offset + data_length * 2]
                    parsed_result = parse_operation_results_19PF(operation_data)
                    if "Filtered" in parsed_result:
                        return {"Filtered": "service category"}
                    else:
                        operation_result.setdefault("Operation Results", []).append(parsed_result)
                        offset += data_length * 2
                else:
                    print(f"[DEBUG] Unknown header code: {header_code}, selected_pf: {get_selected_pf()}")
                    break


            elif "30" <= header_code <= "47":  # Header codes in the range 30 to 47
                data_length = 1  # Default data length for these header codes
                if header_code in ["3A", "42", "44"]:  # 2-byte data
                    data_length = 2
                elif header_code == "3D":  # 3-byte data
                    data_length = 3
                elif header_code == "45":  # 5-byte data
                    data_length = 5

                vehicle_state_data = body_info[offset:offset + data_length * 2]
                vehicle_state_result.setdefault("Vehicle State when Remote A/C", []).append(
                    VEHICLE_STATE_WHEN_REMOTE_AC.get(header_code, lambda _: "Unknown")(vehicle_state_data)
                )
                offset += data_length * 2

            else:
                print(f"[DEBUG] Unknown header code: {header_code}. Skipping. Current offset: {offset}")
                break

        # Return parsed body fields
        return {
            "Position Info Category": position_info_category,
            "Position Info": position_info,
            "Body Info Length": body_info_length,
            "Message Category": message_category,
            "Table Version": table_version_result.get("Table Version", []),
            "Pre-operation Vehicle State": pre_operation_result.get("Pre-operation Vehicle State", []),
            "Time Infomation": time_information_result.get("Time Information", []),
            "Cancel Permission States": cancel_permission_states_result.get("Cancel Permission States", []),
            "Operation Results": operation_result.get("Operation Results", []),
            "Vehicle State when Remote A/C": vehicle_state_result.get("Vehicle State when Remote A/C", [])
        }

    except Exception as e:
        return {"Error": f"Body parsing error: {e}"}
