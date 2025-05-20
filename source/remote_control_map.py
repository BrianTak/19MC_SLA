from config import get_selected_pf  # Import selected_pf from config

SERVICE_TYPE_TABLE_19PF = {
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
    "90": "PIN notification system",
    "F2": "Status notification (Screen response)",
    "F0": "Common",
    "0E": "Seat arrange",
    "0F": "Digital key registration",
    "A4": "Plug & Charging Setting"
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
    "01": lambda param: {
        0b0010: "Car finder start",
        0b0100: "SW ON",
        0b0101: "SW OFF",
    }.get(param, "Unknown"),
    "02": lambda param: {
        0b0001: "Door lock (no Security set)",
        0b0010: "Door unlock (no Security unset)",
        0b0101: "Door lock (with Security set)",
        0b0110: "Door unlock (with Security unset)",
    }.get(param, "Unknown"),
    "03": lambda param: {
        0b0000: "Deleted",
    }.get(param, "Unknown"),
    "05": lambda param: {
        0b001: "Pre-Air conditioning start",
        0b010: "Pre-Air conditioning stop",
        0b011: "Setting change",
    }.get(param, "Unknown"),
    "06": lambda param: {
        0b0001: "Remote start",
        0b0010: "Immobilizer release",
    }.get(param, "Unknown"),
    "07": lambda param: {
        0b0001: "Security set",
        0b0010: "Security unset",
        0b0101: "Alarm condition cancellation *2",
        0b0110: "Alarm condition cancellation release *2",
    }.get(param, "Unknown"),
    "08": lambda param: {
        0b0001: "Buzzer",
    }.get(param, "Unknown"),
    "20": lambda param: {
        0b0001: "Notification start",
        0b0010: "Notification end",
        0b0011: "ASCII data",
        0b0100: "BCD data",
        0b0101: "Binary data",
    }.get(param, "Unknown"),
    "22": lambda param: {
        0b0001: "Progress bar",
    }.get(param, "Unknown"),
    "30": lambda param: {
        0b0011: "Start by Smart key trigger",
        0b0100: "Stop due to vehicle cause",
        0b0101: "Remote air conditioning start",
        0b0110: "Remote air conditioning stop",
    }.get(param, "Unknown"),
    "37": lambda param: {
        0b0011: "Start by Smart key trigger",
        0b0100: "Stop due to vehicle cause",
        0b0101: "Remote air conditioning start",
        0b0110: "Remote air conditioning stop",
    }.get(param, "Unknown"),
    "38": lambda param: {
        0b0001: "Remote air conditioning setting request",
    }.get(param, "Unknown"),
    "39": lambda param: {
        0b0001: "Remote air conditioning setting request",
    }.get(param, "Unknown"),
    "40": lambda param: {
        0b0001: "Smart key verification",
    }.get(param, "Unknown"),
    "41": lambda param: {
        0b0001: "Drive start",
        0b0010: "Drive stop",
    }.get(param, "Unknown"),
    "42": lambda param: {
        "Notification": "Allowed" if int(param, 16) & 0b1000 >> 4 == 1 else "Not allowed",
        "Pre-Air conditioning": "Start" if int(param, 16) & 0b0011 == 0b0001 else "Stop" if int(param, 16) & 0b0011 == 0b0010 else "Setting change" if int(param, 16) & 0b0011 == 0b0011 else "Unknown"
    },
    "44": lambda param: {
        0b0001: "Data upload request",
    }.get(param, "Unknown"),
    "90": lambda param: {
        0b0001: "Remote immobilizer",
    }.get(param, "Unknown"),
    "F2": lambda param: {
        0b0001: "Screen status",
    }.get(param, "Unknown"),
    "F0": lambda param: "Reserved",
    "0E": lambda param: {
        0x0: "Not Request",
        0x1: "Cooperation Seat Support (Walk/In)",
        0x2: "Cooperation Seat Support (Return)",
        0x3: "Cooperation Seat Expansion Mode (Return)",
        0x4: "Cooperation Seat Expansion Mode (Expansion)",
        0x5: "Cooperation Seat arrange pattern",
        0xF: "Stop",
    }.get(param, "Undefined"),
    "0F": lambda param: {
        0b0001: "Digital key registration",
    }.get(param, "Unknown"),
    "A4": lambda param: {
        0b0000: "Plug&Charging setting request",
    }.get(param, "Unknown"),
}

COMMAND_CONTENT_TABLE_15PF = {
    "01": lambda param: {
        0b0010: "Car finder start",
        0b0011: "Car finder stop",
        0b0100: "SW ON",
        0b0101: "SW OFF",
    }.get(param, "Unknown"),
    "02": lambda param: {
        0b0001: "Door lock (no Security set)",
        0b0010: "Door unlock (no Security unset)",
        0b0101: "Door lock (with Security set)",
        0b0110: "Door unlock (with Security unset)",
    }.get(param, "Unknown"),
    "03": lambda param: {
        0b0001: "All closed",
        0b0011: "Undo",
    }.get(param, "Unknown"),
    "37": lambda param: {
        0b0011: "Start by Smart key trigger",
        0b0100: "Stop due to vehicle cause",
        0b0101: "Remote air conditioning start",
        0b0110: "Remote air conditioning stop",
    }.get(param, "Unknown"),
    "38": lambda param: {
        0b0001: "Remote air conditioning setting request",
    }.get(param, "Unknown"),
}

COMMAND_CONTENT_TABLE_19PFv2 = {
    "02": lambda param: {
        0b0001: "Door lock (no Security set)",
        0b0010: "Door unlock (no Security unset)",
        0b0101: "Door lock (with Security set)",
        0b0110: "Door unlock (with Security unset)",
        0b1001: "Windows open",
        0b1010: "Windows close",
    }.get(param, "Unknown"),
}

INDICATOR_TABLE_19PF = {
    "01": lambda param: {
        "Headlight": {'ON' if int(param, 16) & 0b01000000 else 'OFF'},
        "Hazard": {'Applicable' if int(param, 16) & 0b00100000 else 'Not applicable'}
    },
    "02": lambda param: {
        "All doors": "Applicable" if int(param, 16) & 0b10000000 else "Not applicable"
    },
    "03": lambda param: {
        "D-seat": "Applicable" if int(param, 16) & 0b10000000 else "Not applicable",
        "P-seat": "Applicable" if int(param, 16) & 0b01000000 else "Not applicable",
        "RR-seat": "Applicable" if int(param, 16) & 0b00100000 else "Not applicable",
        "RL-seat": "Applicable" if int(param, 16) & 0b00010000 else "Not applicable"
    },
    "05": lambda param: {
        "01": "Air conditioning ECU",
        "02": "Equipment remote start ECU",
        "10": "DCM",
        "20": "Verification ECU",
        "30": "Plug-in ECU"
    }.get(param, "Unknown"),
    "06": lambda param: "Indication target: Undefined",
    "07": lambda param: {
        "Alarm condition": "Applicable" if int(param, 16) & 0b01000000 else "Not applicable"
    },
    "08": lambda param: {
        "Wireless buzzer": "Applicable" if int(param, 16) & 0b10000000 else "Not applicable",
        "Deleted": bin(int(param, 16) & 0b01000000)[2:].zfill(1),
        "Undefined": bin(int(param, 16) & 0b00111111)[2:].zfill(6)
    },
    "20": lambda param: {
        "01": "DCM",
        "03": "AVN",
        "04": "MET"
    }.get(param, "Unknown"),
    "22": lambda param: {
        "01": "AVN",
        "02": "MET",
    }.get(param, "Unknown"),
    "30": lambda param: {
        "02": "Air conditioning ECU",
        "10": "DCM"
    }.get(param, "Unknown"),
    "37": lambda param: {
        "02": "Air conditioning ECU",
        "10": "DCM"
    }.get(param, "Unknown"),
    "38": lambda param: {
        "01": "Air conditioning ECU"
    }.get(param, "Unknown"),
    "39": lambda param: {
        "01": "Air conditioning ECU",
    }.get(param, "Unknown"),
    "40": lambda param: {
        "Smart key verification": "Applicable" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Not applicable"
    },
    "41": lambda param: {
        "Intrusion sensor": "Applicable" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Not applicable"
    },
    "42": lambda param: {
        "10": "DCM",
        "20": "Verification ECU",
        "30": "Plug-in ECU"
    }.get(param, "Unknown"),
    "44": lambda param: {
        "01": "DCM"
    }.get(param, "Unknown"),
    "90": lambda param: {
        "01": "DCM"
    }.get(param, "Unknown"),
    "F2": lambda param: {
        "00": "Not specified",
    }.get(param, "Unknown"),
    "F0": lambda param: "Reserved",
    "0E": lambda param: {
        "Cooperation Seat master ECU": "Applicable" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Not applicable (N/A)",
        "Undefined": bin(int(param, 16) & 0b01111111)[2:].zfill(7)
    },
    "0F": lambda param: {
        "01": "Verification master ECU",
    }.get(param, "Unknown"),
    "A4": lambda param: {
        "Integrated charging ECU": "Applicable" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Not applicable",
        "Undefined": bin(int(param, 16) & 0b01111111)[2:].zfill(7)
    },
}

INDICATOR_TABLE_15PF = {
    "01": lambda param: {
        "Hazard": 'Applicable' if int(param, 16) & 0b00100000 else 'Not applicable'
    },
    "02": lambda param: {
        "All doors": 'Applicable' if int(param, 16) & 0b10000000 else 'Not applicable'
    },
    "37": {
        "02": "Air conditioning ECU",
        "10": "DCM"
    },
    "38": {
        "01": "Air conditioning ECU"
    }
}

REQUEST_PARAM_1_TABLE_19PF = {
    "01": lambda param: {
        "Lights ON": "Yes" if (int(param, 16) & 0b10000000) >> 7 == 1 else "No",
        "Blinking Time": f"{int(param, 16) & 0b01111111} sec"
    },
    "05": lambda param: {
        "Set temperature indicated value": {
            0x00: "MAX COLD",
            0x37: "MAX HOT",
            0x3D: "No start blower",
            0x3E: "Center value start (Auto mode)",
            0x3F: "No temperature change designated",
        }.get(int(param, 16),
            f"{16.0 + (int(param, 16) - 0x01) * 0.5:.1f} degrees C" if 0x01 <= int(param, 16) <= 0x21 else
            f"{14.0 + (int(param, 16) - 0x60) * 0.5:.1f} degrees C" if 0x60 <= int(param, 16) <= 0x63 else
            f"{65 + (int(param, 16) - 0x22)} degrees F" if 0x22 <= int(param, 16) <= 0x36 else
            f"{58 + (int(param, 16) - 0x64)} degrees F" if 0x64 <= int(param, 16) <= 0x6A else
            f"{86 + (int(param, 16) - 0x6B)} degrees F" if 0x6B <= int(param, 16) <= 0x6F else
            "Reserved"
        )
    },
    "06": lambda param: {
        "DRLK output request": {
            0b0000: "No request",
            0b0001: "Lock request",
        }.get((int(param, 16) & 0b11110000) >> 4, "Unknown"),
        "KLEG output request": "E/G being started" if (int(param, 16) & 0b00000100) >> 2 == 0 else "E/G stopped",
        "EGST output request": "Request OFF" if (int(param, 16) & 0b00000010) >> 1 == 0 else "Request ON",
        "REMOTE output request": "Communication interrupted" if int(param, 16) & 0b00000001 == 0 else "Communication not interrupted"
    },
    "07": lambda param: {
        "All sensors": "Applicable" if int(param, 16) & 0b10000000 else "Not applicable",
        "Intrusion sensor front seat": "Applicable" if int(param, 16) & 0b01000000 else "Not applicable"
    },
    "08": lambda param: {
        "Wireless buzzer beep pattern": {
            0x07: "7 (2 sec continuous beep)",
            0x0E: "14",
        }.get((int(param, 16) & 0b11110000) >> 4, "unknown pattern"),
        "Wireless buzzer beep count": f"{int(param, 16) & 0b00001111} times"
    },
    "20": lambda param: {
        "Data 1": int(param, 16)
    },
    "22": lambda param: {
        "Progress rate": f"{int(param, 16) * 100 // 0x64} %"
    },
    "30": lambda param: {
        "Engine Start Permission": "Permit" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Not to permit",
        "Remote Start Operation Time Designation": {
            0x00: "10 minutes (Default)",
        }.get((int(param, 16) & 0b01111111),
            f"{int(param, 16) & 0b01111111} minutes" if 0x01 <= (int(param, 16) & 0b01111111) <= 0x14 else "Reserved"
        )
    },
    "37": lambda param: {
        "Engine start permission": "Permit" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Not to permit",
        "Remote Start Operation Time Designation": {
            0x00: "10 minutes (Default)",
        }.get((int(param, 16) & 0b01111111),
            f"{int(param, 16) & 0b01111111} minutes" if 0x01 <= (int(param, 16) & 0b01111111) <= 0x14 else "Reserved"
        )
    },
    "38": lambda param: {
        "Set temperature indicated value": {
            0x00: "MAX COLD",
            0x37: "MAX HOT",
            0x3D: "No start blower",
            0x3E: "Center value start (Auto mode)",
            0x3F: "No temperature change designated",
        }.get(int(param, 16),
            f"{16.0 + (int(param, 16) - 0x01) * 0.5:.1f} degrees C" if 0x01 <= int(param, 16) <= 0x21 else
            f"{14.0 + (int(param, 16) - 0x60) * 0.5:.1f} degrees C" if 0x60 <= int(param, 16) <= 0x63 else
            f"{65 + (int(param, 16) - 0x22)} degrees F" if 0x22 <= int(param, 16) <= 0x36 else
            f"{58 + (int(param, 16) - 0x64)} degrees F" if 0x64 <= int(param, 16) <= 0x6A else
            f"{86 + (int(param, 16) - 0x6B)} degrees F" if 0x6B <= int(param, 16) <= 0x6F else
            "Reserved"
        )
    },
    "39": lambda param: "Reserved",
    "40": lambda param: "Reserved",
    "41": lambda param: "Reserved",
    "44": lambda param: {
        0x01: "Digital key delete result notification",
    }.get(param, "Unknown"),
    "90": lambda param: {
        0x01: "Process start",
        0x02: "Number verification request",
        0x03: "Process end",
    }.get(param, "Unknown"),
    "F2": lambda param: {
        "User operation": {
            0b00: "None",
            0b01: "Enter",
            0b10: "Cancel",
            0b11: "Reserve",
        }.get((param & 0b11000000) >> 6, "Unknown"),
        "Display status": {
            0b00: "Request not made",
            0b01: "Request under reception another screen display",
            0b10: "Request denied",
            0b11: "Request screen being displayed",
        }.get((param & 0b00110000) >> 4, "Unknown"),
        "Diagnostics mode": "Regular mode" if (param & 0b00001000) >> 3 == 0 else "Diagnostics mode",
        "Screen synchronization counter": (param & 0b00000110) >> 1
    },
    "F0": lambda param: "Reserved",
    "0E": lambda param: {
        "Rr 1-R seat": "Applicable" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Not applicable (N/A)",
        "Rr 1-L seat": "Applicable" if (int(param, 16) & 0b01000000) >> 6 == 1 else "Not applicable (N/A)",
        "Rr 2-R seat": "Applicable" if (int(param, 16) & 0b00100000) >> 5 == 1 else "Not applicable (N/A)",
        "Rr 2-L seat": "Applicable" if (int(param, 16) & 0b00010000) >> 4 == 1 else "Not applicable (N/A)",
        "Undefined": bin(int(param, 16) & 0b00001111)[2:].zfill(4)
    },
    "0F": lambda param: {
        "New key registration request": "Request" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Not request",
        "Undefined": bin(int(param, 16) & 0b01111111)[2:].zfill(7)
    },
    "A4": lambda param: {
        "Notice of Vehicle certificate updating": "With notice" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Less notice",
        "Notice of PE Private Root CA certificate updating": "With notice" if (int(param, 16) & 0b01000000) >> 6 == 1 else "Less notice",
        "Notice of V2G root certificate updating": "With notice" if (int(param, 16) & 0b00100000) >> 5 == 1 else "Less notice",
        "Notice of OEM provisioning certificate updating": "With notice" if (int(param, 16) & 0b00010000) >> 4 == 1 else "Less notice",
        "Request of contract certificate delete": "With notice" if (int(param, 16) & 0b00001000) >> 3 == 1 else "Less notice",
        "Notice of contract certificate updating": "With notice" if (int(param, 16) & 0b00000100) >> 2 == 1 else "Less notice",
        "PnC Setting Change Request": {
            0b00: "No setting change request",
            0b01: "OFF",
            0b10: "ON",
        }.get(int(param, 16) & 0b00000011, "Unknown")
    },
}

REQUEST_PARAM_2_TABLE_19PF = {
    "01": lambda param: {
        "Brightness Level": int(param, 16) & 0b00001111
    },
    "05": lambda param: {
        "Front Defogger": "Request made" if int(param, 16) & 0b10000000 else "No request made",
        "Rear Defogger": "Request made" if int(param, 16) & 0b01000000 else "No request made",
        "Mirror Heater": "Request made" if int(param, 16) & 0b00100000 else "No request made",
        "Front D Seat Heater": "Request made" if int(param, 16) & 0b00010000 else "No request made",
        "Front P Seat Heater": "Request made" if int(param, 16) & 0b00001000 else "No request made",
        "Rear D Seat Heater": "Request made" if int(param, 16) & 0b00000100 else "No request made",
        "Rear P Seat Heater": "Request made" if int(param, 16) & 0b00000010 else "No request made",
        "Steering Heater": "Request made" if int(param, 16) & 0b00000001 else "No request made"
    },
    "06": lambda param: {
        "STSW output request": "STSW output request made" if (int(param, 16) & 0b10000000) >> 7 == 1 else "No STSW output request",
        "HZRD output request": "Lights OFF" if (int(param, 16) & 0b00000100) >> 2 == 0 else "Blinking",
        "DFON output request": "OFF" if (int(param, 16) & 0b00000010) >> 1 == 0 else "ON",
        "ACON output request": "OFF" if int(param, 16) & 0b00000001 == 0 else "ON"
    },
    "07": lambda param: "Reserved",
    "08": lambda param: {
        "Volume": "Maximum volume" if int(param, 16) & 0b00000111 == 0 else int(param, 16) & 0b00000111
    },
    "20": lambda param: {
        "Data 2": int(param, 16)
    },
    "22": lambda param: "Reserved",
    "30": lambda param: {
        "below 5°C": "Turn ON" if (int(param, 16) & 0b00000100) >> 2 == 1 else "Not to turn ON",
        "5-30°C": "Turn ON" if (int(param, 16) & 0b00000010) >> 1 == 1 else "Not to turn ON",
        "above 30°C": "Turn ON" if int(param, 16) & 0b00000001 == 1 else "Not to turn ON"
    },
    "37": lambda param: {
        "Below 5°C": "Turn ON" if (int(param, 16) & 0b00000100) >> 2 == 1 else "Not to turn ON",
        "5-30°C": "Turn ON" if (int(param, 16) & 0b00000010) >> 1 == 1 else "Not to turn ON",
        "Above 30°C": "Turn ON" if int(param, 16) & 0b00000001 == 1 else "Not to turn ON"
    },
    "38": lambda param: {
        "Front Defogger": "Request made" if int(param, 16) & 0b10000000 else "No request made",
        "Rear Defogger": "Request made" if int(param, 16) & 0b01000000 else "No request made",
        "Mirror Heater": "Request made" if int(param, 16) & 0b00100000 else "No request made",
        "Front D Seat Heater": "Request made" if int(param, 16) & 0b00010000 else "No request made",
        "Front P Seat Heater": "Request made" if int(param, 16) & 0b00001000 else "No request made",
        "Rear D Seat Heater": "Request made" if int(param, 16) & 0b00000100 else "No request made",
        "Rear P Seat Heater": "Request made" if int(param, 16) & 0b00000010 else "No request made",
        "Steering Heater": "Request made" if int(param, 16) & 0b00000001 else "No request made"
    },
    "39": lambda param: {
        "Front D Seat Ventilation": "Request made" if int(param, 16) & 0b10000000 else "No request made",
        "Front P Seat Ventilation": "Request made" if int(param, 16) & 0b01000000 else "No request made",
        "Rear D Seat Ventilation": "Request made" if int(param, 16) & 0b00100000 else "No request made",
        "Rear P Seat Ventilation": "Request made" if int(param, 16) & 0b00010000 else "No request made",
        "Reserved": bin(int(param, 16) & 0b00001111)[2:].zfill(4)
    },
    "40": lambda param: {
        "Vehicle inside area": "Applicable" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Not applicable",
        "Definition prohibited": (int(param, 16) & 0b00000111) >> 3
    },
    "41": lambda param: "Reserved",
    "44": lambda param: {
        "Vehicle Delete Result Notification": "No notification" if (int(param, 16) & 0b10000000) >> 7 == 0 else "Notification",
        "Reserved": bin(int(param, 16) & 0b01111111)[2:].zfill(7)
    },
    "90": lambda param: "Reserved",
    "F2": lambda param: {
        "Display screen ID": f"{param:02X}"
    },
    "F0": lambda param: "Reserved",
    "0E": lambda param: {
        0x0: "Not Request",
        0x1: "Pattern 1 (Return)",
        0x2: "Pattern 2 (Expansion)",
        0x3: "Pattern 3",
        0x4: "Pattern 4",
        0x5: "Pattern 5",
        0x6: "Pattern 6",
        0x7: "Pattern 7",
        0x8: "Pattern 8",
        0x9: "Pattern 9",
        0xA: "Pattern 10",
        0xB: "Pattern 11",
        0xC: "Pattern 12",
        0xD: "Pattern 13",
        0xE: "Pattern 14",
        0xF: "Pattern 15",
    }.get(param, "Undefined"),
    "0F": lambda param: "Undefined",
    "A4": lambda param: (
        f"Undefined: {bin(int(param, 16) & 0b11111110)[2:].zfill(7)}, "
        f"Notice of OEM Root CA certificate updating: {'With notice' if (int(param, 16) & 0b00000001) == 1 else 'Less notice'}"
    ),
}

REQUEST_PARAM_2_TABLE_15PF = {
    "01": lambda param: "Operation prerequisite: IG=OFF or Charging" if int(param, 16) & 0b00000001 == 0b00 else "Undefined",
}

PRE_OPERATION_VEHICLE_TABLE_19PF = {
    "01": lambda param: {
        "Power Supply State": "Valid" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Invalid",
        "Normal": "Yes" if (int(param, 16) & 0b01000000) >> 6 == 1 else "No",
        "IG State": "ON" if (int(param, 16) & 0b00100000) >> 5 == 1 else "OFF",
        "ACC State": "ON" if (int(param, 16) & 0b00010000) >> 4 == 1 else "OFF"
    },
    "10": lambda param: {
        "Door Courtesy State": "Valid" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Invalid",
        "Normal": "Yes" if (int(param, 16) & 0b01000000) >> 6 == 1 else "No",
        "Driver Door": "Open" if (int(param, 16) & 0b00100000) >> 5 == 1 else "Closed",
        "Passenger Door": "Open" if (int(param, 16) & 0b00010000) >> 4 == 1 else "Closed",
        "Rear Right Door": "Open" if (int(param, 16) & 0b00001000) >> 3 == 1 else "Closed",
        "Rear Left Door": "Open" if (int(param, 16) & 0b00000100) >> 2 == 1 else "Closed",
        "Back Door": "Open" if (int(param, 16) & 0b00000010) >> 1 == 1 else "Closed"
    },
    "11": lambda param: {
        "Luggage Compartment Courtesy State": "Valid" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Invalid",
        "Normal": "Yes" if (int(param, 16) & 0b01000000) >> 6 == 1 else "No",
        "Luggage Compartment": "Open" if (int(param, 16) & 0b00100000) >> 5 == 1 else "Closed"
    },
    "12": lambda param: {
        "Hood Courtesy State": "Valid" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Invalid",
        "Normal": "Yes" if (int(param, 16) & 0b01000000) >> 6 == 1 else "No",
        "Hood": "Open" if (int(param, 16) & 0b00100000) >> 5 == 1 else "Closed"
    },
    "13": lambda param: {
        "Glass Hatch State": "Valid" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Invalid",
        "Normal": "Yes" if (int(param, 16) & 0b01000000) >> 6 == 1 else "No",
        "Glass Hatch": "Open" if (int(param, 16) & 0b00100000) >> 5 == 1 else "Closed"
    },
    "20": lambda param: {
        "Door Lock Position State": "Valid" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Invalid",
        "Normal": "Yes" if (int(param, 16) & 0b01000000) >> 6 == 1 else "No",
        "Driver Door": "Unlock" if (int(param, 16) & 0b00100000) >> 5 == 1 else "Lock",
        "Passenger Door": "Unlock" if (int(param, 16) & 0b00010000) >> 4 == 1 else "Lock",
        "Rear Right Door": "Unlock" if (int(param, 16) & 0b00001000) >> 3 == 1 else "Lock",
        "Rear Left Door": "Unlock" if (int(param, 16) & 0b00000100) >> 2 == 1 else "Lock",
        "Back Door": "Unlock" if (int(param, 16) & 0b00000010) >> 1 == 1 else "Lock"
    },
    "21": lambda param: {
        "Hazard Lamps State": "Valid" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Invalid",
        "Normal": "Yes" if (int(param, 16) & 0b01000000) >> 6 == 1 else "No",
        "Hazard Lamps SW": "ON" if (int(param, 16) & 0b00100000) >> 5 == 1 else "OFF"
    },
    "22": lambda param: {
        "Driver Door PW State": "Valid" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Invalid",
        "Normal": "Yes" if (int(param, 16) & 0b01000000) >> 6 == 1 else "No",
        "Open/Close State": "Undetermined" if (int(param, 16) & 0b00110000) >> 4 == 0b00 else
                          "Completely open" if (int(param, 16) & 0b00110000) >> 4 == 0b01 else
                          "Completely closed" if (int(param, 16) & 0b00110000) >> 4 == 0b10 else
                          "Other position"
    },
    "23": lambda param: {
        "Passenger Door PW State": "Valid" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Invalid",
        "Normal": "Yes" if (int(param, 16) & 0b01000000) >> 6 == 1 else "No",
        "Open/Close State": "Undetermined" if (int(param, 16) & 0b00110000) >> 4 == 0b00 else
                          "Completely open" if (int(param, 16) & 0b00110000) >> 4 == 0b01 else
                          "Completely closed" if (int(param, 16) & 0b00110000) >> 4 == 0b10 else
                          "Other position"
    },
    "24": lambda param: {
        "Rear Right Door PW State": "Valid" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Invalid",
        "Normal": "Yes" if (int(param, 16) & 0b01000000) >> 6 == 1 else "No",
        "Open/Close State": "Undetermined" if (int(param, 16) & 0b00110000) >> 4 == 0b00 else
                          "Completely open" if (int(param, 16) & 0b00110000) >> 4 == 0b01 else
                          "Completely closed" if (int(param, 16) & 0b00110000) >> 4 == 0b10 else
                          "Other position"
    },
    "25": lambda param: {
        "Rear Left Door PW State": "Valid" if (int(param, 16) & 0b10000000) >> 7 == 1 else "Invalid",
        "Normal": "Yes" if (int(param, 16) & 0b01000000) >> 6 == 1 else "No",
        "Open/Close State": "Undetermined" if (int(param, 16) & 0b00110000) >> 4 == 0b00 else
                          "Completely open" if (int(param, 16) & 0b00110000) >> 4 == 0b01 else
                          "Completely closed" if (int(param, 16) & 0b00110000) >> 4 == 0b10 else
                          "Other position"
    },
}

CANCEL_PERMISSION_STATES_15PF = {
    "A0": lambda param: (
        f"Hazard lamps OFF cancel permission state: {'Cancel permission start' if (int(param[:2], 16) & 0b11000000) >> 6 == 0b11 else 'Cancel permission' if (int(param[:2], 16) & 0b11000000) >> 6 == 0b10 else 'Cancel not permitted' if (int(param[:2], 16) & 0b11000000) >> 6 == 0b00 else 'Unknown'}, "
        f"Lock cancel permission state: {'Cancel permission start' if (int(param[:2], 16) & 0b00110000) >> 4 == 0b11 else 'Cancel permission' if (int(param[:2], 16) & 0b00110000) >> 4 == 0b10 else 'Cancel not permitted' if (int(param[:2], 16) & 0b00110000) >> 4 == 0b00 else 'Unknown'}, "
        f"PW close cancel permission state: {'Cancel permission start' if (int(param[:2], 16) & 0b00001100) >> 2 == 0b11 else 'Cancel permission' if (int(param[:2], 16) & 0b00001100) >> 2 == 0b10 else 'Cancel not permitted' if (int(param[:2], 16) & 0b00001100) >> 2 == 0b00 else 'Unknown'}"
    ),
}

VEHICLE_STATE_WHEN_REMOTE_AC_19PF = {
    "30": lambda param: {
        "Header Code": "30",
        "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
        "Driver Door": "Open" if (int(param, 16) & 0b00100000) >> 5 else "Closed",
        "Passenger Door": "Open" if (int(param, 16) & 0b00010000) >> 4 else "Closed",
        "RR Door": "Open" if (int(param, 16) & 0b00001000) >> 3 else "Closed",
        "RL Door": "Open" if (int(param, 16) & 0b00000100) >> 2 else "Closed",
        "Back Door": "Open" if (int(param, 16) & 0b00000010) >> 1 else "Closed"
    },
    "31": lambda param: {
        "Header Code": "31",
        "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
        "Luggage Compartment": "Open" if (int(param, 16) & 0b00100000) >> 5 else "Closed"
    },
    "32": lambda param: {
        "Header Code": "32",
        "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
        "Hood": "Open" if (int(param, 16) & 0b00100000) >> 5 else "Closed"
    },
    "33": lambda param: {
        "Header Code": "33",
        "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
        "Key Code Confirmation": "Confirmed" if (int(param, 16) & 0b00100000) >> 5 else "Not Confirmed"
    },
    "34": lambda param: {
        "Header Code": "34",
        "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
        "Remote Start Stop Request": "Stop Request" if (int(param, 16) & 0b00100000) >> 5 else "No Request"
    },
    "35": lambda param: {
        "Header Code": "35",
        "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
        "Push Start SW Signal": "ON" if (int(param, 16) & 0b00100000) >> 5 else "OFF"
    },
    "36": lambda param: {
        "Header Code": "36",
        "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
        "Security Control Signal": {
            "Tail Lamp & Head Lamp Alarm": "Request" if (int(param, 16) & 0b10000000) else "No Request",
            "Panic Alarm": "Active" if (int(param, 16) & 0b00100000) else "Inactive",
            "Horn Alarm": "Request" if (int(param, 16) & 0b01000000) else "No Request",
            "Hazard Lamps Alarm": "Request" if (int(param, 16) & 0b00010000) else "No Request"
        }
    },
    "37": lambda param: {
        "Header Code": "37",
        "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
        "Power Supply Mode": {
            0b00: "Normal Mode",
            0b01: "Remote A/C Mode",
            0b10: "Remote Start Mode",
            0b11: "Undefined"
        }.get((int(param, 16) & 0b00110000) >> 4, "Unknown")
    },
    "38": lambda param: {
        "Header Code": "38",
        "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
        "Driver Door Lock": "Unlocked" if (int(param, 16) & 0b00100000) >> 5 else "Locked",
        "Passenger Door Lock": "Unlocked" if (int(param, 16) & 0b00010000) >> 4 else "Locked",
        "RR Door Lock": "Unlocked" if (int(param, 16) & 0b00001000) >> 3 else "Locked",
        "RL Door Lock": "Unlocked" if (int(param, 16) & 0b00000100) >> 2 else "Locked",
        "Back Door Lock": "Unlocked" if (int(param, 16) & 0b00000010) >> 1 else "Locked"
    },
    "39": lambda param: {
        "Header Code": "39",
        "Valid Bit": 0,
        "Normal Bit": 0,
        "Shift Position P Signal": "Fixed to 0"
    },
    "3A": lambda param: {
        "Header Code": "3A",
        "Valid Bit": (int(param[:2], 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param[:2], 16) & 0b01000000) >> 6,
        "Vehicle Speed": f"{int(param[2:], 16)} km/h"
    },
    "3B": lambda param: {
        "Header Code": "3B",
        "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
        "STP SW Disconnection": "Disconnected" if (int(param, 16) & 0b00100000) >> 5 else "Normal",
        "STP SW Signal": "Pushed" if (int(param, 16) & 0b00010000) >> 4 else "Normal"
    },
    "3C": lambda param: {
        "Header Code": "3C",
        "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
        "READY State Signal": "ON" if (int(param, 16) & 0b00100000) >> 5 else "OFF",
        "HV System Error": "Warning" if (int(param, 16) & 0b00010000) >> 4 else "No Warning"
    },
    "3D": lambda param: {
        "Header Code": "3D",
        "Valid Bit": (int(param[:2], 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param[:2], 16) & 0b01000000) >> 6,
        "Engine Speed": f"{int(param[2:], 16)} RPM"
    },
    "3E": lambda param: {
        "Header Code": "3E",
        "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
        "Starter OFF Permission": "Permit" if (int(param, 16) & 0b00100000) >> 5 else "Prohibit"
    },
    "3F": lambda param: {
        "Header Code": "3F",
        "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
        "Remote Start Control": "Active" if (int(param, 16) & 0b00100000) >> 5 else "Inactive"
    },
    "40": lambda param: {
        "Header Code": "40",
        "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
        "Check Engine Warning": "Display" if (int(param, 16) & 0b00100000) >> 5 else "No Display"
    },
    "41": lambda param: {
        "Header Code": "41",
        "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
        "ACC Signal": "ON" if (int(param, 16) & 0b00100000) >> 5 else "OFF",
        "IG SW Signal": "ON" if (int(param, 16) & 0b00010000) >> 4 else "OFF"
    },
    "42": lambda param: {
        "Header Code": "42",
        "Valid Bit": (int(param[:2], 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param[:2], 16) & 0b01000000) >> 6,
        "A/C State": {
            0b00: "Compressor OFF",
            0b01: "Undefined",
            0b10: "Compressor ON",
            0b11: "Full Auto"
        }.get((int(param[:2], 16) & 0b00110000) >> 4, "Unknown"),
        "Outside Temperature": f"{int(param[2:], 16)} °C"
    },
    "43": lambda param: {
        "Header Code": "43",
        "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
        "Glass Hatch": "Open" if (int(param, 16) & 0b00100000) >> 5 else "Closed"
    },
    "44": lambda param: {
        "Header Code": "44",
        "Valid Bit": (int(param[:2], 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param[:2], 16) & 0b01000000) >> 6,
        "Shift States": {
            "P": (int(param[:2], 16) & 0b00100000) >> 5,
            "D": (int(param[:2], 16) & 0b00010000) >> 4,
            "B": (int(param[:2], 16) & 0b00001000) >> 3,
            "N": (int(param[:2], 16) & 0b00000100) >> 2,
            "R": (int(param[:2], 16) & 0b00000010) >> 1,
            "LO": int(param[:2], 16) & 0b00000001
        }
    },
    "45": lambda param: {
        "Header Code": "45",
        "Valid Bit 1": (int(param[:2], 16) & 0b10000000) >> 7,
        "Normal Bit 1": (int(param[:2], 16) & 0b01000000) >> 6,
        "Accelerator Opening": f"{int(param[2:4], 16) * 0.5}%",
        "Valid Bit 2": (int(param[4:6], 16) & 0b10000000) >> 7,
        "Normal Bit 2": (int(param[4:6], 16) & 0b01000000) >> 6,
        "Pedal Angle": f"{int(param[6:8], 16) * 0.5}%",
        "Reliability Info": "Error" if (int(param[8:10], 16) & 0b00100000) >> 5 else "Normal"
    },
    "46": lambda param: {
        "Header Code": "46",
        "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
        "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
        "Remote Air Condition End Request": "Request" if (int(param, 16) & 0b00100000) >> 5 else "No Request"
    },
    "47": lambda param: {
        "PARK Status": {
            "Valid Bit": (int(param, 16) & 0b10000000) >> 7,
            "Normal Bit": (int(param, 16) & 0b01000000) >> 6,
            "Status": "Parked" if (int(param, 16) & 0b00110000) >> 4 == 1 else "Not Parked",
            "Door Lock Factor": {
                0b0000: "No factor",
                0b0001: "Keyless",
                0b0010: "Mechanical key",
                0b0011: "Near-range",
                0b0100: "Mid-range",
                0b0101: "Far-range",
                0b0111: "Auto"
            }.get(int(param, 16) & 0b00001111, "Unknown")
        }
    }
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
    "01": {
        0xD0: "Request discarded due to hazard lamps SW state (OFF)",
        0xD1: "Request discarded due to hazard lamps SW state (ON)",
        0xE0: "Request discarded due to local operation occurrence (simultaneous occurrence)",
        0xE1: "Currently satisfying the Remote hazard operation prohibition condition",
    },
    "02": {
        0xD0: "Request discarded due to door lock position state (all doors locked)",
        0xD1: "Request discarded due to door lock position state (any door unlocked)",
        0xE0: "Request discarded due to local operation occurrence (simultaneous occurrence)",
        0xE1: "Lock operation not complete",
        0xE2: "Unlock operation not complete",
        0xE5: "Currently satisfying the Remote door lock operation prohibition condition",
        0xE6: "Lock cancel request discarded due to security setting state",
    },
    "03": {
        0xD0: "Request discarded due to PW state (all doors closed)",
        0xD1: "Request discarded due to PW state (any door is not closed)",
        0xE0: "Request discarded due to local operation occurrence (simultaneous occurrence)",
        0xE1: "Jam problem occurrence (opened before operation).",
        0xE2: "Jam problem occurrence (closed before operation)",
        0xE3: "Failure detection 2",
        0xE4: "PW operation not possible state (power supply state)",
        0xE5: "Failure detection 1",
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
    "OE": {
        0xD0: "Interference with other request",
        0xD1: "Jamming",
        0xE0: "Success (Stopped for stop request)",
        0xE1: "Stopped for slave error",
    },
    "OF": {
        0xD0: "Failure(BLE not registration)",
        0xD1: "Failure(System abnormal)",
    }
}

STOP_CAUSE_TABLE_19PF = {}

def merge_tables(base_table, table_15pf, table_19pfv2):
    if get_selected_pf() == "15PF":
        return {**base_table, **table_15pf}
    elif get_selected_pf() == "19PFv2":
        return {**base_table, **table_19pfv2}
    return base_table

SERVICE_TYPE_TABLE = merge_tables(SERVICE_TYPE_TABLE_19PF, {}, {})
COMMAND_TYPE_TABLE = merge_tables(COMMAND_TYPE_TABLE_19PF, {}, {})
COMMAND_CONTENT_TABLE = merge_tables(COMMAND_CONTENT_TABLE_19PF, COMMAND_CONTENT_TABLE_15PF, COMMAND_CONTENT_TABLE_19PFv2)
INDICATOR_TABLE = merge_tables(INDICATOR_TABLE_19PF, INDICATOR_TABLE_15PF, {})
REQUEST_PARAM_1_TABLE = merge_tables(REQUEST_PARAM_1_TABLE_19PF, {}, {})
REQUEST_PARAM_2_TABLE = merge_tables(REQUEST_PARAM_2_TABLE_19PF, REQUEST_PARAM_2_TABLE_15PF, {})
PRE_OPERATION_VEHICLE_TABLE = merge_tables(PRE_OPERATION_VEHICLE_TABLE_19PF, {}, {})
VEHICLE_STATE_WHEN_REMOTE_AC = merge_tables(VEHICLE_STATE_WHEN_REMOTE_AC_19PF, {}, {})
RESULT_CODE_TABLE = merge_tables(RESULT_CODE_TABLE_19PF, {}, {})
STOP_CAUSE_TABLE = merge_tables(STOP_CAUSE_TABLE_19PF, {}, {})
CANCEL_PERMISSION_STATES = merge_tables({}, CANCEL_PERMISSION_STATES_15PF, {})
