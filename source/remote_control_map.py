from config import selected_pf  # Import selected_pf from config

SERVICE_TYPE_TABLE = {
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

COMMAND_TYPE_TABLE_19PF = {
    "Request": {
        0b000: "Request not requiring Response",
        0b011: "Request requiring 'Received response' and 'End response'",
    },
    "Response": {
        0b001: "Received Response",
        0b010: "End Response",
    },
}

COMMAND_CONTENT_TABLE_19PF = {
    "01": {
        0b0010: "Car finder start",
        0b0100: "SW ON",
        0b0101: "SW OFF",
    },
    "02": {
        0b0001: "Door lock (no Security set)",
        0b0010: "Door unlock (no Security unset)",
        0b0101: "Door lock (with Security set)",
        0b0110: "Door unlock (with Security unset)",
    },
    "03": {
        # deleted
    },
    "05": {
        0b001: "Pre-Air conditioning start",
        0b010: "Pre-Air conditioning stop",
        0b011: "Setting change"
    },
    "37": {
        0b0011: "Start by Smart key trigger",
        0b0100: "Stop due to vehicle cause",
        0b0101: "Remote air conditioning start",
        0b0110: "Remote air conditioning stop",
    },
    "38": {
        0b0001: "Remote air conditioning setting request",
    },
}

COMMAND_CONTENT_TABLE_19PFv2 = {
    "02": {
        0b0001: "Door lock (no Security set)",
        0b0010: "Door unlock (no Security unset)",
        0b0101: "Door lock (with Security set)",
        0b0110: "Door unlock (with Security unset)",
        0b1001: "Windows open",
        0b1010: "Windows close",
    }
}

COMMAND_CONTENT_TABLE_15PF = {
    "01": {
        0b0010: "Car finder start",
        0b0011: "Car finder stop",
        0b0100: "SW ON",
        0b0101: "SW OFF",
    },
    "02": {
        0b0001: "Door lock (no Security set)",
        0b0010: "Door unlock (no Security unset)",
        0b0101: "Door lock (with Security set)",
        0b0110: "Door unlock (with Security unset)",
    },
    "03": {
        0b0001: "All closed",
        0b0011: "Undo",
    },
    "37": {
        0b0011: "Start by Smart key trigger",
        0b0100: "Stop due to vehicle cause",
        0b0101: "Remote air conditioning start",
        0b0110: "Remote air conditioning stop",
    },
    "38": {
        0b0001: "Remote air conditioning setting request",
    },
}

INDICATOR_TABLE_19PF = {
    "01": lambda param: (
        f"Headlight: {'ON' if int(param, 16) & 0b01000000 else 'OFF'}, "
        f"Hazard: {'Applicable' if int(param, 16) & 0b00100000 else 'Not applicable'}"
    ),
    "02": lambda param: (
        f"All doors: {'Applicable' if int(param, 16) & 0b10000000 else 'Not applicable'}"
    ),
    "03": lambda param: (
        f"D-seat: {'Applicable' if int(param, 16) & 0b10000000 else 'Not applicable'}, "
        f"P-seat: {'Applicable' if int(param, 16) & 0b01000000 else 'Not applicable'}, "
        f"RR-seat: {'Applicable' if int(param, 16) & 0b00100000 else 'Not applicable'}, "
        f"RL-seat: {'Applicable' if int(param, 16) & 0b00010000 else 'Not applicable'}"
    ),
    "05": lambda param: {
        "01": "Air conditioning ECU",
        "02": "Equipment remote start ECU",
        "10": "DCM",
        "20": "Verification ECU",
        "30": "Plug-in ECU"
    }.get(param, "Unknown"),
    "37": lambda param: {
        "02": "Air conditioning ECU",
        "10": "DCM"
    }.get(param, "Unknown"),
    "38": lambda param: {
        "01": "Air conditioning ECU"
    }.get(param, "Unknown")
}

INDICATOR_TABLE_15PF = {
    "01": lambda param: f"Hazard: {'Applicable' if int(param, 16) & 0b00100000 else 'Not applicable'}",
    "02": lambda param: (
        f"All doors: {'Applicable' if int(param, 16) & 0b10000000 else 'Not applicable'}, "
    ),
    "37": {
        "02": "Air conditioning ECU",
        "10": "DCM"
    },
    "38": {
        "01": "Air conditioning ECU"
    }
}

REQUEST_PARAM_1_TABLE_19PF = {
    "01": lambda param: (
        f"Lights ON: {'Yes' if (int(param, 16) & 0b10000000) >> 7 == 1 else 'No'}, "
        f"Blinking Time: {int(param, 16) & 0b01111111} sec"
    ),
    "37": lambda param: (
        f"Engine Start Permission: {'Permit' if (int(param, 16) & 0b10000000) >> 7 == 1 else 'Not to permit'}, "
        f"Remote Start Operation Time: {('10mins (Default)' if (int(param, 16) & 0b01111111) == 0x00 else f'{int(param, 16) & 0b01111111}mins') if 0x01 <= (int(param, 16) & 0b01111111) <= 0x14 else 'Reserved'}"
    ),
    "38": lambda param: (
        "MAX COLD" if int(param, 16) == 0x00 else
        "MAX HOT" if int(param, 16) == 0x37 else
        "No start blower" if int(param, 16) == 0x3D else
        "Center value start (Auto mode)" if int(param, 16) == 0x3E else
        "No temperature change designated" if int(param, 16) == 0x3F else
        f"{16.0 + (int(param, 16) - 0x01) * 0.5:.1f} degrees C" if 0x01 <= int(param, 16) <= 0x21 else
        f"{14.0 + (int(param, 16) - 0x60) * 0.5:.1f} degrees C" if 0x60 <= int(param, 16) <= 0x63 else
        f"{65 + (int(param, 16) - 0x22)} degrees F" if 0x22 <= int(param, 16) <= 0x36 else
        f"{58 + (int(param, 16) - 0x64)} degrees F" if 0x64 <= int(param, 16) <= 0x6A else
        f"{86 + (int(param, 16) - 0x6B)} degrees F" if 0x6B <= int(param, 16) <= 0x6F else
        "Reserved"
    ),
    "05": lambda param: (
        "MAX COLD" if int(param, 16) == 0x00 else
        "MAX HOT" if int(param, 16) == 0x37 else
        "No start blower" if int(param, 16) == 0x3D else
        "Center value start (Auto mode)" if int(param, 16) == 0x3E else
        "No temperature change designated" if int(param, 16) == 0x3F else
        f"{16.0 + (int(param, 16) - 0x01) * 0.5:.1f} degrees C" if 0x01 <= int(param, 16) <= 0x21 else
        f"{14.0 + (int(param, 16) - 0x60) * 0.5:.1f} degrees C" if 0x60 <= int(param, 16) <= 0x63 else
        f"{65 + (int(param, 16) - 0x22)} degrees F" if 0x22 <= int(param, 16) <= 0x36 else
        f"{58 + (int(param, 16) - 0x64)} degrees F" if 0x64 <= int(param, 16) <= 0x6A else
        f"{86 + (int(param, 16) - 0x6B)} degrees F" if 0x6B <= int(param, 16) <= 0x6F else
        "Reserved"
    ),
}

REQUEST_PARAM_1_TABLE_15PF = {

}

REQUEST_PARAM_2_TABLE_19PF = {
    "01": lambda param: f"Brightness Level: {int(param, 16) & 0b00001111}",
    "37": lambda param: (
        f"below 5°C: {'Turn ON' if (int(param, 16) & 0b00000100) >> 2 == 1 else 'Not to turn ON'}, "
        f"5-30°C: {'Turn ON' if (int(param, 16) & 0b00000010) >> 1 == 1 else 'Not to turn ON'}, "
        f"above 30°C: {'Turn ON' if int(param, 16) & 0b00000001 == 1 else 'Not to turn ON'}"
    ),
    "38": lambda param: (
        f"Front Defogger: {'Request made' if int(param, 16) & 0b10000000 else 'No request made'}, "
        f"Rear Defogger: {'Request made' if int(param, 16) & 0b01000000 else 'No request made'}, "
        f"Mirror Heater: {'Request made' if int(param, 16) & 0b00100000 else 'No request made'}, "
        f"Front D Seat Heater: {'Request made' if int(param, 16) & 0b00010000 else 'No request made'}, "
        f"Front P Seat Heater: {'Request made' if int(param, 16) & 0b00001000 else 'No request made'}, "
        f"Rear D Seat Heater: {'Request made' if int(param, 16) & 0b00000100 else 'No request made'}, "
        f"Rear P Seat Heater: {'Request made' if int(param, 16) & 0b00000010 else 'No request made'}, "
        f"Steering Heater: {'Request made' if int(param, 16) & 0b00000001 else 'No request made'}"
    ),
    "05": lambda param: (
        f"Front Defogger: {'Request made' if int(param, 16) & 0b10000000 else 'No request made'}, "
        f"Rear Defogger: {'Request made' if int(param, 16) & 0b01000000 else 'No request made'}, "
        f"Mirror Heater: {'Request made' if int(param, 16) & 0b00100000 else 'No request made'}, "
        f"Front D Seat Heater: {'Request made' if int(param, 16) & 0b00010000 else 'No request made'}, "
        f"Front P Seat Heater: {'Request made' if int(param, 16) & 0b00001000 else 'No request made'}, "
        f"Rear D Seat Heater: {'Request made' if int(param, 16) & 0b00000100 else 'No request made'}, "
        f"Rear P Seat Heater: {'Request made' if int(param, 16) & 0b00000010 else 'No request made'}, "
        f"Steering Heater: {'Request made' if int(param, 16) & 0b00000001 else 'No request made'}"
    ),
}

REQUEST_PARAM_2_TABLE_15PF = {
    "01": lambda param: "Operation prerequisite: IG=OFF or Charging" if int(param, 16) & 0b00000001 == 0b00 else "Undefined",

}

RESULT_CODE_TABLE_19PF = {
    "00": {
        0x01: "Success",
        0x02: "During operation",
        0x10: "Request discarded due to request error (request combination error)",
        0x11: "Request discarded due to request error (unspecified command)",
        0x12: "Request discarded due to request error (request arrival delay)",
        0x13: "Request discarded due to request error (request time error)",
        0x20: "Request discarded due to out-of-standby time",
        0x30: "Request discarded due to cancel operation not possible (initial state)",
        0x31: "Request discarded due to cancel operation not possible (1 day elapsed)",
        0x32: "Request discarded due to cancel operation not possible (IG/ACC ON)",
        0x33: "Request discarded due to cancel operation not possible (local operation occurrence)",
        0x34: "Request discarded due to cancel operation not possible (after cancel success)",
        0x35: "Request discarded due to cancel operation not possible (normal operation failure)",
        0x40: "Request discarded due to vehicle being driven",
        0x41: "Request discarded due to during repair reject",
        0x42: "Request discarded due to initial setting not complete",
        0x43: "Request discarded due to different random number reception",
        0x50: "Request discarded due to local operation occurrence (pre-occurrence)",
        0x60: "Request discarded due to vehicle operation (door opened)",
        0x61: "Request discarded due to vehicle operation (luggage compartment opened)",
        0x62: "Request discarded due to vehicle operation (hood opened)",
        0x63: "Request discarded due to vehicle operation (door lock operation)",
        0x70: "Request discarded due to key detected in cabin (key present)",
        0x71: "Request discarded due to key detected in cabin (Smart cancel)",
        0x72: "Request discarded due to key detected in cabin (verification not possible state)",
        0x80: "Request discarded due to intrusion sensor error detection.",
        0x81: "Request discarded due to intrusion sensor response present",
        0xC0: "Request discarded due to vehicle error (time acquisition disruption)",
        0xC1: "Request discarded due to vehicle error (time acquisition error)",
        0xC2: "Request discarded due to vehicle error (periodic communication disruption)",
        0xC3: "Request discarded due to vehicle error (periodic transmission error).",
        0xC4: "Request discarded due to vehicle error (response disruption 1)",
        0xC5: "Request discarded due to vehicle error (response error 1)",
        0xC6: "Request discarded due to DCM error",
    },
    "37": {
        0xD0: "Request discarded due to during stop operation",
        0xD1: "Request discarded due to start-up conditions not satisfied",
        0xD2: "Request discarded due to DCM power supply voltage drop",
        0xD3: "Request discarded due to remote start integrated time elapse",
        0xD4: "Request discarded due to ongoing start-up",
        0xD5: "Request discarded due to ongoing accessory remote start connection",
        0xD6: "Start-up stopped due to stop request reception",
        0xD7: "Request discarded due to not during remote start start-up",
        0xD8: "Stopped due to key operation",
        0xD9: "Stopped due to vehicle factor",
        0xDA: "Stopped due to start-up time upper limit reached",
        0xDB: "Stopped due to power supply voltage drop",
        0xDC: "Key operation start-up success",
        0xDD: "Key operation start-up failure",
        0xDE: "Stopped due to remote parking system request",
        0xDF: "Request rejected due to H2 or BATT-SOC Low",
        0xE0: "Immobilizer release communication failure",
        0xE1: "Power supply control failure",
        0xE2: "Stopped due to H2 or BATT-SOC Low",
        0xE3: "Stopped due to drive away",
        0xE4: "Request rejected due to Engine start not to permit",
        0xF0: "Start control failure",
        0xF1: "Stop control failure",
    },
    "38": {
        # Add specific result codes for service type "38" here if needed
    },
}

STOP_CAUSE_TABLE_19PF = {
    "00": {
    },
    "37": {
    },
}

# SERVICE_TYPE_TABLE = SERVICE_TYPE_TABLE if selected_pf == "19PF" else {}
COMMAND_CONTENT_TABLE = (
    COMMAND_CONTENT_TABLE_15PF if selected_pf == "15PF"
    else {**COMMAND_CONTENT_TABLE_19PF, **COMMAND_CONTENT_TABLE_19PFv2} if selected_pf == "19PFv2"
    else COMMAND_CONTENT_TABLE_19PF
)

INDICATOR_TABLE = (
    INDICATOR_TABLE_15PF if selected_pf == "15PF"
    else INDICATOR_TABLE_19PF
)

REQUEST_PARAM_1_TABLE = (
    REQUEST_PARAM_1_TABLE_15PF if selected_pf == "15PF"
    else REQUEST_PARAM_1_TABLE_19PF
)

REQUEST_PARAM_2_TABLE = (
    REQUEST_PARAM_2_TABLE_15PF if selected_pf == "15PF"
    else REQUEST_PARAM_2_TABLE_19PF
)

RESULT_CODE_TABLE = (
    RESULT_CODE_TABLE_19PF if selected_pf == "19PF" or selected_pf == "19PFv2"
    else {}
)

STOP_CAUSE_TABLE = (
    STOP_CAUSE_TABLE_19PF if selected_pf == "19PF" or selected_pf == "19PFv2"
    else {}
)