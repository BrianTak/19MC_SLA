# Renamed to `file_handler.py` for better clarity
import pandas as pd
from tkinter import filedialog, messagebox
from tkinter import StringVar
import os
from util.database import (
    get_original_data,
    set_original_data,
)

# 하드코딩된 xlsx 파일 경로
HARDCODED_XLSX_PATH = "sample/5YFB4MDE1RP156769_0115-0315.xlsx"
USE_HARDCODED_XLSX = False  # Flag to toggle between hardcoded xlsx and file dialog

def load_file():
    """
    Opens a file dialog to load a CSV or Excel file and returns the loaded data and file name.

    Returns:
        tuple: (pd.DataFrame, str) The loaded data as a DataFrame and the file name.
    """
    file_path = filedialog.askopenfilename(
        filetypes=[("All Files", "*.*")],
    )
    if not file_path:
        return None, None

    try:
        if file_path.endswith(".csv"):
            data = pd.read_csv(file_path)
        elif file_path.endswith((".xlsx", ".xls")):
            data = pd.read_excel(file_path)
        else:
            messagebox.showerror("Error", "Unsupported file format.")
            return None, None

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")
        return None, None

    return data, file_path

# 파일 로드 핸들러 함수
def handle_load_file():
    global data
    try:
        if USE_HARDCODED_XLSX:
            # Load the hardcoded xlsx file
            set_original_data(pd.read_excel(HARDCODED_XLSX_PATH))
            file_name = os.path.basename(HARDCODED_XLSX_PATH)
        else:
            data, file_name = load_file()
            if not file_name:
                return None # User canceled the file dialog
            set_original_data(data)

        if get_original_data() is not None:
            return file_name

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")
        return None