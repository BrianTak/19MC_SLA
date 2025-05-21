# Renamed to `file_handler.py` for better clarity
import pandas as pd
from tkinter import filedialog, messagebox

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