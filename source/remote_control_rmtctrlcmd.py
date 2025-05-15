from remote_control_common import (
    parse_time_information,
    parse_option
)

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


