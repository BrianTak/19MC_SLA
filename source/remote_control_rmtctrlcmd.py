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

def interpret_light_command(command_bit):
    """
    Interprets the command contents for the Light System.

    Args:
        command_bit (int): The command contents value (binary representation as an integer).

    Returns:
        str: A description of the command contents.
    """
    if command_bit == 0b0010:
        return "Car finder start"
    elif command_bit == 0b0011:
        return "Car finder stop"
    elif command_bit == 0b0100:
        return "SW ON"
    elif command_bit == 0b0101:
        return "SW OFF"
    else:
        return "Unknown Command"


def interpret_light_target(target_byte):
    """
    Interprets the indication target for the Light System.

    Args:
        target_byte (str): The indication target value as a hexadecimal string.

    Returns:
        str: A description of the indication target.
    """
    target_mapping = {
        "01": "Light ECU",
        "02": "Main Body ECU"
    }
    return target_mapping.get(target_byte, "Unknown Target")


def interpret_light_parameter_1(param_byte):
    """
    Interprets parameter 1 for the Light System.

    Args:
        param_byte (str): The parameter 1 value as a hexadecimal string.

    Returns:
        str: A description of parameter 1.
    """
    param = int(param_byte, 16)
    light_status = "ON" if param & 0b00000001 else "OFF"
    return f"Light Status: {light_status}"


def interpret_light_parameter_2(param_byte):
    """
    Interprets parameter 2 for the Light System.

    Args:
        param_byte (str): The parameter 2 value as a hexadecimal string.

    Returns:
        str: A description of parameter 2.
    """
    param = int(param_byte, 16)
    brightness_level = param & 0b00001111  # Extract bits 0-3
    return f"Brightness Level: {brightness_level}"

# Renamed to `air_conditioning_interpreter.py` for clarity

def interpret_ac_command(command_bit):
    """
    Interprets the command contents for the Remote Air Conditioning System.

    Args:
        command_bit (int): The command contents value (binary representation as an integer).

    Returns:
        str: A description of the command contents.
    """
    if command_bit == 0b0011:
        return "Start by Smart key trigger"
    elif command_bit == 0b0100:
        return "Stop due to vehicle cause"
    elif command_bit == 0b0101:
        return "Remote air conditioning start"
    elif command_bit == 0b0110:
        return "Remote air conditioning stop"
    else:
        return "Unknown Command"


def interpret_ac_target(target_byte):
    """
    Interprets the indication target for the Remote Air Conditioning System.

    Args:
        target_byte (str): The indication target value as a hexadecimal string.

    Returns:
        str: A description of the indication target.
    """
    target_mapping = {
        "02": "Air conditioning ECU",
        "10": "DCM"
    }
    return target_mapping.get(target_byte, "Unknown Target")


def interpret_ac_parameter_1(param_byte):
    """
    Interprets parameter 1 for the Remote Air Conditioning System.

    Args:
        param_byte (str): The parameter 1 value as a hexadecimal string.

    Returns:
        str: A description of parameter 1.
    """
    param = int(param_byte, 16)
    engine_start_permission = (param & 0b10000000) >> 7  # Extract bit 7
    operation_time = param & 0b01111111  # Extract bits 6-0

    engine_start_desc = "ON" if engine_start_permission == 1 else "OFF"
    if operation_time == 0x00:
        operation_time_desc = "10mins(D)"
    elif 0x01 <= operation_time <= 0x14:
        operation_time_desc = f"{operation_time}mins"
    else:
        operation_time_desc = "Reserved"

    return f"Engine Start: {engine_start_desc}, Time: {operation_time_desc}"


def interpret_ac_parameter_2(param_byte):
    """
    Interprets parameter 2 for the Remote Air Conditioning System.

    Args:
        param_byte (str): The parameter 2 value as a hexadecimal string.

    Returns:
        str: A description of parameter 2.
    """
    param = int(param_byte, 16)
    below_5 = (param & 0b00000100) >> 2  # Extract bit 2
    between_5_and_30 = (param & 0b00000010) >> 1  # Extract bit 1
    above_30 = param & 0b00000001  # Extract bit 0

    below_5_desc = "ON" if below_5 == 1 else "OFF"
    between_5_and_30_desc = "ON" if between_5_and_30 == 1 else "OFF"
    above_30_desc = "ON" if above_30 == 1 else "OFF"

    return f"<5°C: {below_5_desc}, 5-30°C: {between_5_and_30_desc}, >30°C: {above_30_desc}"


def interpret_service_type(service_type_byte):
    """
    Interprets the service type based on the service_type_byte.

    Args:
        service_type_byte (str): The service type value as a hexadecimal string.

    Returns:
        str: A description of the service type in the format "byte값 (결과값)".
    """
    service_type_mapping = {
        "00": "N/A",
        "01": "Light system",
        "02": "Door lock・encrypted system",
        "03": "Window system",
        "05": "Air conditioning system",
        "06": "Remote start system",
        "07": "Security system",
        "08": "Buzzer system",
        "20": "Text data system",
        "22": "Progress system",
        "30": "Remote air conditioning system",
        "37": "Remote air conditioning system Ver.2",
        "38": "Remote air conditioning system Ver.2 air conditioning settings(1)",
        "39": "Remote air conditioning system Ver.2 air conditioning settings(2)",
        "40": "Smart key verification system",
        "41": "Sensor drive system",
        "42": "Air conditioning status notification system (vehicle initiated)",
        "44": "Data upload request",
        "90": "PIN notification",
        "F2": "Status notification (Screen response)",
        "F0": "Common"
    }

    # Get the result from the mapping
    result = service_type_mapping.get(service_type_byte, "Unknown Service Type")

    # Truncate the result if it's longer than 10 characters
    if len(result) > 15:
        result = result[:15] + "..."

    # Format the output as "byte값 (결과값)"
    return f"{service_type_byte} ({result})"

def interpret_command_type(req_res, command_type_bit):
    """
    Interprets the command type based on the Request/Response bit and command_type_bit.

    Args:
        req_res (str): "Request" or "Response".
        command_type_bit (int): The mode value (binary representation as an integer).

    Returns:
        str: A description of the command type in the format "bit값 (결과)".
    """
    if req_res == "Request":
        if command_type_bit == 0b000:
            result = "Request not requiring Response"
        elif command_type_bit == 0b011:
            result = "Request requiring 'Received response' and 'End response'"
        else:
            result = "Unknown Request Mode"
    elif req_res == "Response":
        if command_type_bit == 0b001:
            result = "Received Response"
        elif command_type_bit == 0b010:
            result = "End Response"
        else:
            result = "Unknown Response Mode"
    else:
        result = "Invalid"

    # Format the output as "bit값 (결과)"
    bit_value = f"{command_type_bit:03b}"  # Convert to 3-bit binary
    if len(result) > 15:  # Truncate if the result is longer than 15 characters
        result = result[:15] + "..."
    return f"{bit_value} ({result})"

def interpret_command_contents(service_type_byte, command_contents_bit):
    """
    Interprets the command contents based on the service_type_byte and command_contents_bit.

    Args:
        service_type_byte (str): The service type value as a hexadecimal string.
        command_contents_bit (int): The command contents value (binary representation as an integer).

    Returns:
        str: A description of the command contents in the format "bit값 (결과값)".
    """
    if service_type_byte == "01":
        result = interpret_light_command(command_contents_bit)
    elif service_type_byte == "37":
        result = interpret_ac_command(command_contents_bit)
    else:
        result = "Unknown"

    # Format the output as "bit값 (결과값)"
    bit_value = f"{command_contents_bit:04b}"  # Convert to 4-bit binary
    if len(result) > 15:  # Truncate if the result is longer than 15 characters
        result = result[:15] + "..."
    return f"{bit_value} ({result})"

def interpret_indication_target(indication_target_byte):
    """
    Interprets the indication target based on the indication_target_byte.

    Args:
        indication_target_byte (str): The indication target value as a hexadecimal string.

    Returns:
        str: A description of the indication target.
    """
    if indication_target_byte == "01":
        return interpret_light_target(indication_target_byte)
    elif indication_target_byte == "37":
        return interpret_ac_target(indication_target_byte)
    else:
        return "Unknown Indication Target"

def interpret_parameter_1(service_type_byte, parameter_1_byte):
    """
    Interprets parameter 1 based on the service_type_byte and parameter_1_byte.

    Args:
        service_type_byte (str): The service type value as a hexadecimal string.
        parameter_1_byte (str): The parameter 1 value as a hexadecimal string.

    Returns:
        str: A description of parameter 1.
    """
    if service_type_byte == "01":
        return interpret_light_parameter_1(parameter_1_byte)
    elif service_type_byte == "37":
        return interpret_ac_parameter_1(parameter_1_byte)
    else:
        return "Unknown"

def interpret_parameter_2(service_type_byte, parameter_2_byte):
    """
    Interprets parameter 2 based on the service_type_byte and parameter_2_byte.

    Args:
        service_type_byte (str): The service type value as a hexadecimal string.
        parameter_2_byte (str): The parameter 2 value as a hexadecimal string.

    Returns:
        str: A description of parameter 2.
    """
    if service_type_byte == "01":
        return interpret_light_parameter_2(parameter_2_byte)
    elif service_type_byte == "37":
        return interpret_ac_parameter_2(parameter_2_byte)
    else:
        return "Unknown"

def parse_option(option_data):
    # Parse fields for each option
    service_type_byte = option_data[0:2]  # 1 byte (2 hex characters)
    service_type = interpret_service_type(service_type_byte)

    command_byte = int(option_data[2:4], 16)  # 1 byte (2 hex characters)

    # Extract Request/Response bit and Interpret Request/Response
    req_res_bit = (command_byte & 0b10000000) >> 7  # Extract 7th bit (Request/Response)
    req_res = "Request" if req_res_bit == 0 else "Response"

    # Extract Command Type bit (4-6 bits) and Interpret Command Type
    command_type_bit = (command_byte & 0b01110000) >> 4  # Extract 4-6 bits (Mode)
    command_type = interpret_command_type(req_res, command_type_bit)

    # Extract Command Contents (0-3 bits) and Interpret Command Contents
    command_contents_bit = command_byte & 0b00001111  # Extract 0-3 bits (Command type)
    command_contents = interpret_command_contents(service_type_byte, command_contents_bit)

    indication_target_byte = option_data[4:6]  # 1 byte (2 hex characters)
    indication_target = interpret_indication_target(indication_target_byte)

    parameter_1_byte = option_data[6:8]
    parameter_1 = interpret_parameter_1(service_type_byte, parameter_1_byte)

    parameter_2_byte = option_data[8:10]
    parameter_2 = interpret_parameter_2(service_type_byte, parameter_2_byte)

    reserve_1 = option_data[10:12]
    reserve_2 = option_data[12:14]

    # Add parsed option to the list
    return{
        "Service Type": service_type,
        "Req/Res": req_res,
        "Command Type": command_type,
        "Command Contents": command_contents,
        "Indication Target": indication_target,
        "Parameter 1": parameter_1,
        "Parameter 2": parameter_2,
        "Reserve 1": reserve_1,
        "Reserve 2": reserve_2,
    }

# Header parsing function
# Parses the header of the resbody data for rmtctrlcmd.
def parse_rmtctrlcmd_header(resbody):
    """
    Parses the header of the resbody data for rmtctrlcmd.

    Args:
        resbody (str): The raw resbody data as a string.

    Returns:
        dict: A dictionary containing the parsed header fields.
    """
    try:
        # Ensure the data is long enough to parse the header
        if len(resbody) < 34:  # Minimum length required for the header
            return {"Error": "Header data too short"}

        # Parse header fields
        command_id = resbody[:2]  # 1 byte (2 hex characters)
        command_id_int = int(resbody[:2], 16)  # Convert command_id to integer
        protocol_version = (command_id_int & 0b01111000) >> 3  # Extract 4-7 bits
        reserved = command_id_int & 0b00000111  # Extract 0-3 bits
        message_id = resbody[2:4]  # 1 byte (2 hex characters)
        request_id = bytes.fromhex(resbody[4:10]).decode('ascii', errors='replace')  # 3 bytes (6 hex characters) converted to ASCII

        # Convert time_of_day to a human-readable format using the common function
        time_of_day = resbody[10:34]  # 12 bytes (24 hex characters)
        time_of_day_formatted = parse_time_information(time_of_day)

        # Return parsed header fields
        return {
            "Command ID": command_id,
            "Protocol Version": protocol_version,
            "Reserved": reserved,
            "Message ID": message_id,
            "Request ID": request_id,
            "Request Date": time_of_day_formatted.get("Time", "N/A")
        }

    except Exception as e:
        return {"Error": f"Parsing error: {e}"}

# Body parsing function
# Parses the body of the resbody data for rmtctrlcmd.
def parse_rmtctrlcmd_body(resbody):
    """
    Parses the body of the resbody data for rmtctrlcmd.

    Args:
        resbody (str): The raw resbody data as a string.

    Returns:
        dict: A dictionary containing the parsed body fields.
    """
    try:
        # Ensure the data is long enough to parse the body
        if len(resbody) < 34:  # Minimum length required for the body
            return {"Error": "Body data too short"}

        # Parse the Option count (1 byte)
        option_count = int(resbody[34:36], 16)  # Start parsing from the 34th byte
        parsed_option = []

        # Loop through each option
        offset = 36  # Start parsing options from the 36th byte
        for _ in range(option_count):
            if len(resbody) < offset + 14:  # Each option is 14 characters (7 bytes)
                return {"Error": "Body data too short"}

            parsed_option.append(parse_option(resbody[offset:offset + 14]))

            # Move to the next option
            offset += 14

        return {
            "Option Count": option_count,
            "Option": parsed_option
        }
    except Exception as e:
        return {"Error": f"Body parsing error: {e}"}


