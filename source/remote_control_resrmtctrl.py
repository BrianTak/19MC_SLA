from remote_control_rmtctrlcmd import (
    parse_option
)

def parse_time_information(data):
    """
    Parses the Time Information data.

    Args:
        data (str): The raw data as a hexadecimal string.

    Returns:
        dict: A dictionary containing the parsed Time Information.
    """
    try:
        if len(data) != 24:  # 12 bytes = 24 hex characters
            return {"Error": "Invalid Time Information length"}

        # Parse year, month, day, hour, minute, second
        year = int(data[:4], 16)
        month = int(data[4:8], 16)
        day = int(data[8:12], 16)
        hour = int(data[12:16], 16)
        minute = int(data[16:20], 16)
        second = int(data[20:24], 16)

        # Format the time as a human-readable string
        time_formatted = f"{year:04}-{month:02}-{day:02} {hour:02}:{minute:02}:{second:02}"

        return {"Time": time_formatted}

    except Exception as e:
        return {"Error": f"Time Information parsing error: {e}"}

def parse_table_version(data):
    """
    Parses the Table Version data.

    Args:
        data (str): The raw data as a hexadecimal string (2 bytes).

    Returns:
        dict: A dictionary containing the parsed Table Version.
    """
    try:
        major_version = int(data[0], 16)  # High nibble
        minor_version = int(data[1], 16)  # Low nibble
        return {
            "Major Version": major_version,
            "Minor Version": minor_version
        }
    except Exception as e:
        return {"Error": f"Parsing error: {e}"}


def parse_pre_operation_vehicle_state(header_code, data):
    """
    Parses the Pre-operation Vehicle State data based on the header code.

    Args:
        header_code (str): The header code indicating the type of data.
        data (str): The raw data as a hexadecimal string.

    Returns:
        dict: A dictionary containing the parsed Pre-operation Vehicle State.
    """
    try:
        if header_code == "01":  # Power Supply State
            power_supply_state = int(data, 16)
            return {
                "Power Supply State": {
                    "Valid Bit": (power_supply_state & 0b10000000) >> 7,
                    "Normal Bit": (power_supply_state & 0b01000000) >> 6,
                    "IG State": "ON" if (power_supply_state & 0b00100000) >> 5 else "OFF",
                    "ACC State": "ON" if (power_supply_state & 0b00010000) >> 4 else "OFF"
                }
            }

        elif header_code == "10":  # Door Courtesy State
            door_courtesy_state = int(data, 16)
            return {
                "Door Courtesy State": {
                    "Valid Bit": (door_courtesy_state & 0b10000000) >> 7,
                    "Normal Bit": (door_courtesy_state & 0b01000000) >> 6,
                    "Driver Door": "Open" if (door_courtesy_state & 0b00100000) >> 5 else "Closed",
                    "Passenger Door": "Open" if (door_courtesy_state & 0b00010000) >> 4 else "Closed",
                    "Rear Right Door": "Open" if (door_courtesy_state & 0b00001000) >> 3 else "Closed",
                    "Rear Left Door": "Open" if (door_courtesy_state & 0b00000100) >> 2 else "Closed",
                    "Back Door": "Open" if (door_courtesy_state & 0b00000010) >> 1 else "Closed"
                }
            }

        elif header_code == "11":  # Luggage Compartment Courtesy State
            luggage_compartment_state = int(data, 16)
            return {
                "Luggage Compartment Courtesy State": {
                    "Valid Bit": (luggage_compartment_state & 0b10000000) >> 7,
                    "Normal Bit": (luggage_compartment_state & 0b01000000) >> 6,
                    "Luggage Compartment": "Open" if (luggage_compartment_state & 0b00100000) >> 5 else "Closed"
                }
            }

        elif header_code == "12":  # Hood Courtesy State
            hood_courtesy_state = int(data, 16)
            return {
                "Hood Courtesy State": {
                    "Valid Bit": (hood_courtesy_state & 0b10000000) >> 7,
                    "Normal Bit": (hood_courtesy_state & 0b01000000) >> 6,
                    "Hood": "Open" if (hood_courtesy_state & 0b00100000) >> 5 else "Closed"
                }
            }

        elif header_code == "13":  # Glass Hatch State
            glass_hatch_state = int(data, 16)
            return {
                "Glass Hatch State": {
                    "Valid Bit": (glass_hatch_state & 0b10000000) >> 7,
                    "Normal Bit": (glass_hatch_state & 0b01000000) >> 6,
                    "Glass Hatch": "Open" if (glass_hatch_state & 0b00100000) >> 5 else "Closed"
                }
            }

        elif header_code == "20":  # Door Lock Position State
            door_lock_position_state = int(data, 16)
            return {
                "Door Lock Position State": {
                    "Valid Bit": (door_lock_position_state & 0b10000000) >> 7,
                    "Normal Bit": (door_lock_position_state & 0b01000000) >> 6,
                    "Driver Door": "Unlock" if (door_lock_position_state & 0b00100000) >> 5 else "Lock",
                    "Passenger Door": "Unlock" if (door_lock_position_state & 0b00010000) >> 4 else "Lock",
                    "Rear Right Door": "Unlock" if (door_lock_position_state & 0b00001000) >> 3 else "Lock",
                    "Rear Left Door": "Unlock" if (door_lock_position_state & 0b00000100) >> 2 else "Lock",
                    "Back Door": "Unlock" if (door_lock_position_state & 0b00000010) >> 1 else "Lock"
                }
            }

        elif header_code == "21":  # Hazard Lamps State
            hazard_lamps_state = int(data, 16)
            return {
                "Hazard Lamps State": {
                    "Valid Bit": (hazard_lamps_state & 0b10000000) >> 7,
                    "Normal Bit": (hazard_lamps_state & 0b01000000) >> 6,
                    "Hazard Lamps SW": "ON" if (hazard_lamps_state & 0b00100000) >> 5 else "OFF"
                }
            }

        elif header_code in ["22", "23", "24", "25"]:  # Window States
            door_pw_state = int(data, 16)
            open_close_state_mapping = {
                0b00: "Undetermined",
                0b01: "Completely open",
                0b10: "Completely closed",
                0b11: "Other position"
            }
            open_close_state = (door_pw_state & 0b00110000) >> 4  # Extract bits 1.5 to 1.4

            door_label = {
                "22": "Driver Door PW State",
                "23": "Passenger Door PW State",
                "24": "Rear Right Door PW State",
                "25": "Rear Left Door PW State"
            }.get(header_code, "Unknown Door")

            return {
                door_label: {
                    "Valid Bit": (door_pw_state & 0b10000000) >> 7,
                    "Normal Bit": (door_pw_state & 0b01000000) >> 6,
                    "Open/Close State": open_close_state_mapping.get(open_close_state, "Unknown")
                }
            }

        else:
            print(f"[DEBUG] Unknown header code: {header_code}. Data: {data}")
            return {"Error": f"Unknown header code: {header_code}"}

    except Exception as e:
        print(f"[DEBUG] Error while parsing header code {header_code} with data {data}: {e}")
        return {"Error": f"Parsing error: {e}"}

def parse_operation_results(data):
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
        # center_service_category = center_request_command[0:2]
        # center_command_byte = int(center_request_command[2:4], 16)
        # center_command_type = (center_command_byte & 0b11110000) >> 4  # Upper 4 bits
        # center_command_contents = center_command_byte & 0b00001111  # Lower 4 bits
        # center_indication_target = center_request_command[4:6]
        # center_parameter_1 = center_request_command[6:8]
        # center_parameter_2 = center_request_command[8:10]
        # center_reserve_1 = center_request_command[10:12]
        # center_reserve_2 = center_request_command[12:14]

        # Parse Operation Result Command (7 bytes)
        operation_result_command = data[14:28]  # 7 bytes = 14 hex chars
        operation_result_command_parsed = parse_option(operation_result_command)
        # result_service_category = operation_result_command[0:2]
        # result_command_byte = int(operation_result_command[2:4], 16)
        # result_command_type = (result_command_byte & 0b11110000) >> 4  # Upper 4 bits
        # result_command_contents = result_command_byte & 0b00001111  # Lower 4 bits
        # result_indication_target = operation_result_command[4:6]
        # result_parameter_1 = operation_result_command[6:8]
        # result_parameter_2 = operation_result_command[8:10]
        # result_reserve_1 = operation_result_command[10:12]
        # result_reserve_2 = operation_result_command[12:14]

        combined_result = {
            "Center Request Command": center_request_command_parsed,
            "Operation Result Command": operation_result_command_parsed
        }

        return combined_result

        # # Return parsed operation result
        # return {
        #     "Center Request Command": {
        #         "Service Category": center_request_command_parsed.get("Service Category", "N/A"),
        #         "Command Type": f"{center_command_type:04b}",
        #         "Command Contents": f"{center_command_contents:04b}",
        #         "Indication Target": center_indication_target,
        #         "Parameter 1": center_parameter_1,
        #         "Parameter 2": center_parameter_2,
        #         "Reserve 1": center_reserve_1,
        #         "Reserve 2": center_reserve_2
        #     },
        #     "Operation Result Command": {
        #         "Service Category": result_service_category,
        #         "Command Type": f"{result_command_type:04b}",
        #         "Command Contents": f"{result_command_contents:04b}",
        #         "Indication Target": result_indication_target,
        #         "Parameter 1": result_parameter_1,
        #         "Parameter 2": result_parameter_2,
        #         "Reserve 1": result_reserve_1,
        #         "Reserve 2": result_reserve_2
        #     }
        # }
    except Exception as e:
        return {"Error": f"Parsing error: {e}"}

def parse_vehicle_state_when_remote_ac(header_code, data):
    """
    Parses the Vehicle State when Remote A/C from the remaining data.

    Args:
        header_code (str): The header code indicating the type of data.
        data (str): The raw data as a hexadecimal string.

    Returns:
        dict: A dictionary containing the parsed vehicle state.
    """
    try:
        # Decode based on Header Code
        if header_code == "30":  # Door Courtesy State
            return {
                "Header Code": header_code,
                "Valid Bit": (int(data, 16) & 0b10000000) >> 7,
                "Normal Bit": (int(data, 16) & 0b01000000) >> 6,
                "Driver Door": "Open" if (int(data, 16) & 0b00100000) >> 5 else "Closed",
                "Passenger Door": "Open" if (int(data, 16) & 0b00010000) >> 4 else "Closed",
                "RR Door": "Open" if (int(data, 16) & 0b00001000) >> 3 else "Closed",
                "RL Door": "Open" if (int(data, 16) & 0b00000100) >> 2 else "Closed",
                "Back Door": "Open" if (int(data, 16) & 0b00000010) >> 1 else "Closed"
            }
        elif header_code == "31":  # Luggage Compartment Courtesy State
            return {
                "Header Code": header_code,
                "Valid Bit": (int(data, 16) & 0b10000000) >> 7,
                "Normal Bit": (int(data, 16) & 0b01000000) >> 6,
                "Luggage Compartment": "Open" if (int(data, 16) & 0b00100000) >> 5 else "Closed"
            }
        elif header_code == "32":  # Hood Courtesy State
            return {
                "Header Code": header_code,
                "Valid Bit": (int(data, 16) & 0b10000000) >> 7,
                "Normal Bit": (int(data, 16) & 0b01000000) >> 6,
                "Hood": "Open" if (int(data, 16) & 0b00100000) >> 5 else "Closed"
            }
        elif header_code == "33":  # Key Code Confirmation Signal State
            return {
                "Header Code": header_code,
                "Valid Bit": (int(data, 16) & 0b10000000) >> 7,
                "Normal Bit": (int(data, 16) & 0b01000000) >> 6,
                "Key Code Confirmation": "Confirmed" if (int(data, 16) & 0b00100000) >> 5 else "Not Confirmed"
            }
        elif header_code == "34":  # Remote Start Stop Request State
            return {
                "Header Code": header_code,
                "Valid Bit": (int(data, 16) & 0b10000000) >> 7,
                "Normal Bit": (int(data, 16) & 0b01000000) >> 6,
                "Remote Start Stop Request": "Stop Request" if (int(data, 16) & 0b00100000) >> 5 else "No Request"
            }
        elif header_code == "35":  # Push Start SW Signal State
            return {
                "Header Code": header_code,
                "Valid Bit": (int(data, 16) & 0b10000000) >> 7,
                "Normal Bit": (int(data, 16) & 0b01000000) >> 6,
                "Push Start SW Signal": "ON" if (int(data, 16) & 0b00100000) >> 5 else "OFF"
            }
        elif header_code == "36":  # Security Control Signal State
            return {
                "Header Code": header_code,
                "Valid Bit": (int(data, 16) & 0b10000000) >> 7,
                "Normal Bit": (int(data, 16) & 0b01000000) >> 6,
                "Security Control Signal": {
                    "Tail Lamp & Head Lamp Alarm": "Request" if (int(data, 16) & 0b10000000) else "No Request",
                    "Panic Alarm": "Active" if (int(data, 16) & 0b00100000) else "Inactive",
                    "Horn Alarm": "Request" if (int(data, 16) & 0b01000000) else "No Request",
                    "Hazard Lamps Alarm": "Request" if (int(data, 16) & 0b00010000) else "No Request"
                }
            }
        elif header_code == "37":  # Power Supply Mode State
            power_mode = (int(data, 16) & 0b00110000) >> 4
            return {
                "Header Code": header_code,
                "Valid Bit": (int(data, 16) & 0b10000000) >> 7,
                "Normal Bit": (int(data, 16) & 0b01000000) >> 6,
                "Power Supply Mode": {
                    0b00: "Normal Mode",
                    0b01: "Remote A/C Mode",
                    0b10: "Remote Start Mode",
                    0b11: "Undefined"
                }.get(power_mode, "Unknown")
            }
        elif header_code == "38":  # Door Lock Position State
            return {
                "Header Code": header_code,
                "Valid Bit": (int(data, 16) & 0b10000000) >> 7,
                "Normal Bit": (int(data, 16) & 0b01000000) >> 6,
                "Driver Door Lock": "Unlocked" if (int(data, 16) & 0b00100000) >> 5 else "Locked",
                "Passenger Door Lock": "Unlocked" if (int(data, 16) & 0b00010000) >> 4 else "Locked",
                "RR Door Lock": "Unlocked" if (int(data, 16) & 0b00001000) >> 3 else "Locked",
                "RL Door Lock": "Unlocked" if (int(data, 16) & 0b00000100) >> 2 else "Locked",
                "Back Door Lock": "Unlocked" if (int(data, 16) & 0b00000010) >> 1 else "Locked"
            }
        elif header_code == "39":  # Shift State
            return {
                "Header Code": header_code,
                "Valid Bit": 0,
                "Normal Bit": 0,
                "Shift Position P Signal": "Fixed to 0"
            }
        elif header_code == "3A":  # Vehicle Speed
            valid_bit = (int(data[:2], 16) & 0b10000000) >> 7
            normal_bit = (int(data[:2], 16) & 0b01000000) >> 6
            vehicle_speed = int(data[2:], 16)  # Remaining 1 byte
            return {
                "Header Code": header_code,
                "Valid Bit": valid_bit,
                "Normal Bit": normal_bit,
                "Vehicle Speed": f"{vehicle_speed} km/h"
            }
        elif header_code == "3B":  # Brake State
            return {
                "Header Code": header_code,
                "Valid Bit": (int(data, 16) & 0b10000000) >> 7,
                "Normal Bit": (int(data, 16) & 0b01000000) >> 6,
                "STP SW Disconnection": "Disconnected" if (int(data, 16) & 0b00100000) >> 5 else "Normal",
                "STP SW Signal": "Pushed" if (int(data, 16) & 0b00010000) >> 4 else "Normal"
            }
        elif header_code == "3C":  # HV System State
            return {
                "Header Code": header_code,
                "Valid Bit": (int(data, 16) & 0b10000000) >> 7,
                "Normal Bit": (int(data, 16) & 0b01000000) >> 6,
                "READY State Signal": "ON" if (int(data, 16) & 0b00100000) >> 5 else "OFF",
                "HV System Error": "Warning" if (int(data, 16) & 0b00010000) >> 4 else "No Warning"
            }
        elif header_code == "3D":  # Engine Speed
            valid_bit = (int(data[:2], 16) & 0b10000000) >> 7
            normal_bit = (int(data[:2], 16) & 0b01000000) >> 6
            engine_speed = int(data[2:], 16)  # Remaining 2 bytes
            return {
                "Header Code": header_code,
                "Valid Bit": valid_bit,
                "Normal Bit": normal_bit,
                "Engine Speed": f"{engine_speed} RPM"
            }
        elif header_code == "3E":  # Starter OFF Permission State
            return {
                "Header Code": header_code,
                "Valid Bit": (int(data, 16) & 0b10000000) >> 7,
                "Normal Bit": (int(data, 16) & 0b01000000) >> 6,
                "Starter OFF Permission": "Permit" if (int(data, 16) & 0b00100000) >> 5 else "Prohibit"
            }
        elif header_code == "3F":  # Remote Start Control State
            return {
                "Header Code": header_code,
                "Valid Bit": (int(data, 16) & 0b10000000) >> 7,
                "Normal Bit": (int(data, 16) & 0b01000000) >> 6,
                "Remote Start Control": "Active" if (int(data, 16) & 0b00100000) >> 5 else "Inactive"
            }
        elif header_code == "40":  # Warning State
            return {
                "Header Code": header_code,
                "Valid Bit": (int(data, 16) & 0b10000000) >> 7,
                "Normal Bit": (int(data, 16) & 0b01000000) >> 6,
                "Check Engine Warning": "Display" if (int(data, 16) & 0b00100000) >> 5 else "No Display"
            }
        elif header_code == "41":  # Power Supply State
            return {
                "Header Code": header_code,
                "Valid Bit": (int(data, 16) & 0b10000000) >> 7,
                "Normal Bit": (int(data, 16) & 0b01000000) >> 6,
                "ACC Signal": "ON" if (int(data, 16) & 0b00100000) >> 5 else "OFF",
                "IG SW Signal": "ON" if (int(data, 16) & 0b00010000) >> 4 else "OFF"
            }
        elif header_code == "42":  # A/C State
            valid_bit = (int(data[:2], 16) & 0b10000000) >> 7
            normal_bit = (int(data[:2], 16) & 0b01000000) >> 6
            ac_state = (int(data[:2], 16) & 0b00110000) >> 4
            ac_state_mapping = {
                0b00: "Compressor OFF",
                0b01: "Undefined",
                0b10: "Compressor ON",
                0b11: "Full Auto"
            }
            outside_temp = int(data[2:], 16)  # Remaining 1 byte
            return {
                "Header Code": header_code,
                "Valid Bit": valid_bit,
                "Normal Bit": normal_bit,
                "A/C State": ac_state_mapping.get(ac_state, "Unknown"),
                "Outside Temperature": f"{outside_temp} °C"
            }
        elif header_code == "43":  # Glass Hatch State
            return {
                "Header Code": header_code,
                "Valid Bit": (int(data, 16) & 0b10000000) >> 7,
                "Normal Bit": (int(data, 16) & 0b01000000) >> 6,
                "Glass Hatch": "Open" if (int(data, 16) & 0b00100000) >> 5 else "Closed"
            }
        elif header_code == "44":  # Shift State
            valid_bit = (int(data[:2], 16) & 0b10000000) >> 7
            normal_bit = (int(data[:2], 16) & 0b01000000) >> 6
            shift_states = {
                "P": (int(data[:2], 16) & 0b00100000) >> 5,
                "D": (int(data[:2], 16) & 0b00010000) >> 4,
                "B": (int(data[:2], 16) & 0b00001000) >> 3,
                "N": (int(data[:2], 16) & 0b00000100) >> 2,
                "R": (int(data[:2], 16) & 0b00000010) >> 1,
                "LO": int(data[:2], 16) & 0b00000001
            }
            return {
                "Header Code": header_code,
                "Valid Bit": valid_bit,
                "Normal Bit": normal_bit,
                "Shift States": shift_states
            }
        elif header_code == "45":  # Accelerator State
            valid_bit_1 = (int(data[:2], 16) & 0b10000000) >> 7
            normal_bit_1 = (int(data[:2], 16) & 0b01000000) >> 6
            accelerator_opening = int(data[2:4], 16) * 0.5  # 1 byte
            valid_bit_2 = (int(data[4:6], 16) & 0b10000000) >> 7
            normal_bit_2 = (int(data[4:6], 16) & 0b01000000) >> 6
            pedal_angle = int(data[6:8], 16) * 0.5  # 1 byte
            reliability_info = (int(data[8:10], 16) & 0b00100000) >> 5
            return {
                "Header Code": header_code,
                "Valid Bit 1": valid_bit_1,
                "Normal Bit 1": normal_bit_1,
                "Accelerator Opening": f"{accelerator_opening}%",
                "Valid Bit 2": valid_bit_2,
                "Normal Bit 2": normal_bit_2,
                "Pedal Angle": f"{pedal_angle}%",
                "Reliability Info": "Error" if reliability_info else "Normal"
            }
        elif header_code == "46":  # Remote Air Condition End Request
            return {
                "Header Code": header_code,
                "Valid Bit": (int(data, 16) & 0b10000000) >> 7,
                "Normal Bit": (int(data, 16) & 0b01000000) >> 6,
                "Remote Air Condition End Request": "Request" if (int(data, 16) & 0b00100000) >> 5 else "No Request"
            }
        elif header_code == "47":  # PARK Status
            park_status = int(data, 16)
            return {
                "PARK Status": {
                    "Valid Bit": (park_status & 0b10000000) >> 7,
                    "Normal Bit": (park_status & 0b01000000) >> 6,
                    "Status": "Parked" if (park_status & 0b00110000) >> 4 == 1 else "Not Parked",
                    "Door Lock Factor": {
                        0b0000: "No factor",
                        0b0001: "Keyless",
                        0b0010: "Mechanical key",
                        0b0011: "Near-range",
                        0b0100: "Mid-range",
                        0b0101: "Far-range",
                        0b0111: "Auto"
                    }.get(park_status & 0b00001111, "Unknown")
                }
            }

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
            offset += 2

            if header_code == "F0":  # Table Version
                data_length = 1  # Table Version is 1 bytes
                table_version_data = body_info[offset:offset + data_length * 2]
                table_version_result.setdefault("Table Version", []).append(
                    parse_table_version(table_version_data)
                )
                offset += data_length * 2

            elif header_code in ["01", "10", "11", "12", "13", "20", "21", "22", "23", "24", "25"]:  # Pre-operation Vehicle State
                data_length = 1  # Each of Pre-operation Vehicle State is 2 bytes
                pre_operation_data = body_info[offset:offset + data_length * 2]
                pre_operation_result.setdefault("Pre-operation Vehicle State", []).append(
                    parse_pre_operation_vehicle_state(header_code, pre_operation_data)
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

            elif header_code in ["D1", "D2", "D3", "D4", "D5", "D6", "D7"]:  # Operation Results
                data_length = 14  # Time Information is 14 bytes
                operation_data = body_info[offset:offset + data_length * 2]
                operation_result.setdefault("Operation Results", []).append(
                    parse_operation_results(operation_data)
                )
                offset += data_length * 2

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
                    parse_vehicle_state_when_remote_ac(header_code, vehicle_state_data)
                )
                offset += data_length * 2

            else:
                print(f"[DEBUG] Unknown header code: {header_code}. Skipping.")
                break

        # Debug log for final results
        # print(f"[DEBUG] Final Table Version Result: {table_version_result}")
        # print(f"[DEBUG] Final Pre-operation Result: {pre_operation_result}")
        # print(f"[DEBUG] Final Time Information Result: {time_information_result}")
        # print(f"[DEBUG] Final Operation Results: {operation_result}")

        # Return parsed body fields
        return {
            "Position Info Category": position_info_category,
            "Position Info": position_info,
            "Body Info Length": body_info_length,
            "Table Version": table_version_result.get("Table Version", []),
            "Pre-operation Vehicle State": pre_operation_result.get("Pre-operation Vehicle State", []),
            "Time Infomation": time_information_result.get("Time Information", []),
            "Operation Results": operation_result.get("Operation Results", []),
            "Vehicle State when Remote A/C": vehicle_state_result.get("Vehicle State when Remote A/C", [])
        }

    except Exception as e:
        return {"Error": f"Body parsing error: {e}"}
