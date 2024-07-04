import os
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import subprocess

def center_window(root):
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def change_modify_date(file_path, new_date):
    timestamp = new_date.timestamp()
    os.utime(file_path, (timestamp, timestamp))

def change_create_date(file_path, new_date):
    formatted_date = new_date.strftime("%Y-%m-%dT%H:%M:%S")
    command = f'(Get-Item "{file_path}").CreationTime=("{formatted_date}")'
    subprocess.run(["powershell", "-Command", command], check=True)

def import_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_path_var.set(file_path)
        update_file_info(file_path)

def update_file_info(file_path):
    file_info = os.stat(file_path)
    created_date = datetime.datetime.fromtimestamp(file_info.st_ctime)
    modified_date = datetime.datetime.fromtimestamp(file_info.st_mtime)
    created_date_var.set(created_date.strftime('%Y-%m-%d %H:%M:%S'))
    modified_date_var.set(modified_date.strftime('%Y-%m-%d %H:%M:%S'))

def clear_input_time():
    year_var.set('')
    month_var.set('')
    day_var.set('')
    hour_var.set('')
    minute_var.set('')
    second_var.set('')

def validate_date(year, month, day):
    try:
        datetime.datetime(year, month, day)
    except ValueError:
        return False
    return True

def apply_changes():
    file_path = file_path_var.get()
    if not file_path:
        messagebox.showerror("Error", "Please select a file first.")
        return

    current_date = datetime.datetime.now()

    if not year_var.get():
        messagebox.showerror("Error", "Missing data in Year field.")
        return
    if not month_var.get():
        messagebox.showerror("Error", "Missing data in Month field.")
        return
    if not day_var.get():
        messagebox.showerror("Error", "Missing data in Day field.")
        return
    if not hour_var.get():
        messagebox.showerror("Error", "Missing data in Hour field.")
        return
    if not minute_var.get():
        messagebox.showerror("Error", "Missing data in Minute field.")
        return
    if not second_var.get():
        messagebox.showerror("Error", "Missing data in Second field.")
        return

    year = int(year_var.get())
    month = int(month_var.get())
    day = int(day_var.get())

    if not validate_date(year, month, day):
        messagebox.showerror("Error", f"Invalid date: {year}-{month}-{day}.")
        return

    new_date = datetime.datetime(
        year, month, day,
        int(hour_var.get()), int(minute_var.get()), int(second_var.get())
    )

    if new_date > current_date:
        messagebox.showerror("Error", "Date cannot be in the future.")
        return
    
    try:
        if action_var.get() == "Created":
            change_create_date(file_path, new_date)
        else:
            change_modify_date(file_path, new_date)
        
        update_file_info(file_path)
        messagebox.showinfo("Success", f"Successfully changed {action_var.get()} date.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("File Date Changer")

main_frame = ttk.Frame(root, padding="5")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

file_path_var = tk.StringVar()
created_date_var = tk.StringVar()
modified_date_var = tk.StringVar()
action_var = tk.StringVar(value="Created")

# Move "Selected File" and "Import File" to the top
ttk.Label(main_frame, text="File:").grid(row=0, column=0, sticky=tk.W, padx=2, pady=2)
ttk.Entry(main_frame, textvariable=file_path_var, width=40).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=2, pady=2)
ttk.Button(main_frame, text="Import", command=import_file).grid(row=0, column=2, padx=2, pady=2)

# Move "Created" and "Modified" radiobuttons to the second row
ttk.Label(main_frame, text="Action:").grid(row=1, column=0, sticky=tk.W, padx=2, pady=2)
action_frame = ttk.Frame(main_frame)
action_frame.grid(row=1, column=1, columnspan=2, sticky=tk.W)
ttk.Radiobutton(action_frame, text="Created", variable=action_var, value="Created").grid(row=0, column=0, padx=2, pady=2)
ttk.Radiobutton(action_frame, text="Modified", variable=action_var, value="Modified").grid(row=0, column=1, padx=2, pady=2)

# Created Date and Modified Date
ttk.Label(main_frame, text="Created:").grid(row=2, column=0, sticky=tk.W, padx=2, pady=2)
ttk.Entry(main_frame, textvariable=created_date_var, state='readonly', width=30).grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=2, pady=2)

ttk.Label(main_frame, text="Modified:").grid(row=3, column=0, sticky=tk.W, padx=2, pady=2)
ttk.Entry(main_frame, textvariable=modified_date_var, state='readonly', width=30).grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=2, pady=2)

# Day, Month, Year
ttk.Label(main_frame, text="Day:").grid(row=4, column=0, sticky=tk.W, padx=2, pady=2)
ttk.Label(main_frame, text="Month:").grid(row=4, column=1, sticky=tk.W, padx=2, pady=2)
ttk.Label(main_frame, text="Year:").grid(row=4, column=2, sticky=tk.W, padx=2, pady=2)

day_var = tk.StringVar()
month_var = tk.StringVar()
year_var = tk.StringVar()
hour_var = tk.StringVar()
minute_var = tk.StringVar()
second_var = tk.StringVar()

current_year = datetime.datetime.now().year
years = list(range(current_year, 1979, -1))

ttk.Combobox(main_frame, textvariable=day_var, values=list(range(1, 32)), width=5).grid(row=5, column=0, sticky=(tk.W, tk.E), padx=2, pady=2)
ttk.Combobox(main_frame, textvariable=month_var, values=list(range(1, 13)), width=5).grid(row=5, column=1, sticky=(tk.W, tk.E), padx=2, pady=2)
ttk.Combobox(main_frame, textvariable=year_var, values=years, width=5).grid(row=5, column=2, sticky=(tk.W, tk.E), padx=2, pady=2)

# Hour, Minute, Second
ttk.Label(main_frame, text="Hour:").grid(row=6, column=0, sticky=tk.W, padx=2, pady=2)
ttk.Label(main_frame, text="Minute:").grid(row=6, column=1, sticky=tk.W, padx=2, pady=2)
ttk.Label(main_frame, text="Second:").grid(row=6, column=2, sticky=tk.W, padx=2, pady=2)

ttk.Combobox(main_frame, textvariable=hour_var, values=list(range(0, 24)), width=5).grid(row=7, column=0, sticky=(tk.W, tk.E), padx=2, pady=2)
ttk.Combobox(main_frame, textvariable=minute_var, values=list(range(0, 60)), width=5).grid(row=7, column=1, sticky=(tk.W, tk.E), padx=2, pady=2)
ttk.Combobox(main_frame, textvariable=second_var, values=list(range(0, 60)), width=5).grid(row=7, column=2, sticky=(tk.W, tk.E), padx=2, pady=2)

button_frame = ttk.Frame(main_frame)
button_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.E), padx=2, pady=2)

ttk.Button(button_frame, text="Clear", command=clear_input_time).grid(row=0, column=0, padx=2, pady=2)
ttk.Button(button_frame, text="Apply", command=apply_changes).grid(row=0, column=1, padx=2, pady=2)

# Center the window
center_window(root)

root.mainloop()
