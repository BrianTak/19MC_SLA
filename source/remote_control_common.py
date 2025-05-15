from remote_control_map import (
    SERVICE_TYPE_TABLE,
    COMMAND_TYPE_TABLE,
    COMMAND_CONTENT_TABLE,
    INDICATOR_TABLE,
    REQUEST_PARAM_1_TABLE,
    REQUEST_PARAM_2_TABLE,
    RESULT_CODE_TABLE,
    STOP_CAUSE_TABLE
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

def merge_result_code_tables(service_type_byte, table):
    base_table = table.get("00", {})
    service_table = table.get(service_type_byte, {})
    merged_table = {**base_table, **service_table}  # Merge dictionaries
    return merged_table

def parse_option(option_data):
    # Parse fields for each option
    service_type_byte = option_data[0:2]  # 1 byte (2 hex characters)
    service_type = SERVICE_TYPE_TABLE.get(service_type_byte, "N/A")

    command_byte = option_data[2:4]  # 1 byte (2 hex characters)

    # Extract Request/Response bit and Interpret Request/Response
    req_res_bit = (int(command_byte, 16) & 0b10000000) >> 7  # Extract 7th bit (Request/Response)
    req_res = "Request" if req_res_bit == 0 else "Response"

    # Extract Command Type bit (4-6 bits) and Interpret Command Type
    command_type_bit = (int(command_byte, 16) & 0b01110000) >> 4  # Extract 4-6 bits (Mode)
    command_type = COMMAND_TYPE_TABLE.get(req_res, {}).get(command_type_bit, "N/A")

    # Extract Command Contents (0-3 bits) and Interpret Command Contents
    command_contents_bit = int(command_byte, 16) & 0b00001111  # Extract 0-3 bits (Command type)
    command_content = COMMAND_CONTENT_TABLE.get(service_type_byte, {}).get(command_contents_bit, "N/A")

    indication_target_byte = option_data[4:6]  # 1 byte (2 hex characters)
    indication_target = INDICATOR_TABLE.get(service_type_byte, lambda _: "Unknown")(indication_target_byte)

    parameter_1_byte = option_data[6:8]  # 1 byte (2 hex characters)
    parameter_2_byte = option_data[8:10]  # 1 byte (2 hex characters)

    if command_type == "End Response":
        param1 = f"Result Code: {int(parameter_1_byte, 16):02X} ({merge_result_code_tables(service_type_byte, RESULT_CODE_TABLE).get(int(parameter_1_byte, 16), 'N/A')})"
        param2 = f"Stop Cause: {int(parameter_2_byte, 16):02X} ({merge_result_code_tables(service_type_byte, STOP_CAUSE_TABLE).get(int(parameter_2_byte, 16), 'N/A')})"
    else:
        param1 = REQUEST_PARAM_1_TABLE.get(service_type_byte, lambda _: "Unknown")(parameter_1_byte)
        param2 = REQUEST_PARAM_2_TABLE.get(service_type_byte, lambda _: "Unknown")(parameter_2_byte)

    reserve_1 = option_data[10:12]
    reserve_2 = option_data[12:14]

    # Interpret based on command type
    return {
        "Service Type": service_type,
        "Req/Res": req_res,
        "Command Type": command_type,
        "Command Contents": command_content,
        "Indication Target": indication_target,
        "Parameter 1": param1,
        "Parameter 2": param2,
        "Reserve 1": reserve_1,
        "Reserve 2": reserve_2,
    }
