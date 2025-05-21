from tkinter import StringVar

SERVICE_FLAG_URL = "http://dcmservice-provisioning-service.local/mc/telematics/srvflg/"
RSCDLCHK_URL = "http://dcmservice-provisioning-service.local/mc/telematics/rscdlchk/"
REMOTE_CONTROL_CMD_URL = "http://dcmservice-remocon-service.local/remoteservices/rmtctrlcmd/"
REMOTE_CONTROL_RESP_URL = "http://dcmservice-remocon-service.local/mc/remoteservices/resrmtctrl/"

# Checkbox Labels
CHECKBOX_LABELS = ["Telematics", "RSFlag", "RmtCtrl", "SVT", "VPPlus", "VP", "Alarm", "RmtImmobi", "RmtConf", "Dormant"]

global selected_pf

# Define selected_pf as a global variable
selected_pf = "19PF"

# Getter and Setter for selected_pf
def get_selected_pf():
    global selected_pf
    return selected_pf

def set_selected_pf(value):
    global selected_pf
    selected_pf = value

selected_service_category = "00"

# Getter and Setter for selected_service_category
def get_selected_service_category():
    global selected_service_category
    return selected_service_category

def set_selected_service_category(value):
    global selected_service_category
    selected_service_category = value

selected_service_flags = []

# Getter and Setter for selected_service_flags
def get_selected_service_flags():
    global selected_service_flags
    return selected_service_flags

def set_selected_service_flags(value):
    global selected_service_flags
    selected_service_flags = value
