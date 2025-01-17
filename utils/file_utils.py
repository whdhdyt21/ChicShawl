import os
import pandas as pd

def read_excel(file_path):
    if not os.path.isfile(file_path):
        return []
    try:
        with pd.ExcelFile(file_path) as xls:
            df = pd.read_excel(xls)
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca file Excel: {e}")
        return []

def write_excel(file_path, data, headers):
    try:
        df = pd.DataFrame(data, columns=headers)
        with pd.ExcelWriter(file_path) as writer:
            df.to_excel(writer, index=False)
    except Exception as e:
        print(f"Terjadi kesalahan saat menulis ke file Excel: {e}")

def append_excel(file_path, row, headers):
    try:
        if not os.path.exists(file_path):
            write_excel(file_path, [row], headers)
        else:
            with pd.ExcelFile(file_path) as xls:
                df = pd.read_excel(xls)
            new_row = pd.DataFrame([row], columns=headers)
            df = pd.concat([df, new_row], ignore_index=True)
            with pd.ExcelWriter(file_path) as writer:
                df.to_excel(writer, index=False)
    except Exception as e:
        print(f"Terjadi kesalahan saat menambahkan ke file Excel: {e}")