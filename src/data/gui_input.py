import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import subprocess
import time
import requests
import os

# --- 1. AUTOMATION: START FLASK SERVER ---
# This starts your time_management.py in the background
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, 'time_management.py')
    server_process = subprocess.Popen(['python', script_path])
    print(f"Starting Flask Server at: {script_path}")
    time.sleep(1) 
except Exception as e:
    print(f"Could not start server: {e}")

def on_closing():
    # --- 2. CLEANUP: STOP SERVER ON EXIT ---
    server_process.terminate()
    root.destroy()

def send_to_api():
    # Combine Date and Time into YYYY-MM-DD HH:MM:SS
    selected_date = cal.get_date()
    start_dt = f"{selected_date} {start_h.get()}:{start_m.get()}:00"
    end_dt = f"{selected_date} {end_h.get()}:{end_m.get()}:00"

    # Match the JSON keys your Flask app expects
    payload = {
        "consultant_id": entry_cons_id.get(),
        "customer_id": entry_cust_id.get(),
        "start_time": start_dt,
        "end_time": end_dt,
        "lunchbreak": var_lunch.get()
    }

    url = "http://127.0.0.1:5000/add-hours"
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 201:
            messagebox.showinfo("Success", "Data logged to Azure Database!")
        else:
            messagebox.showerror("Error", f"Server returned: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Connection Error", "Is the Flask server running?")

# --- 3. GUI LAYOUT ---
root = tk.Tk()
root.title("Azure Time Management System")
root.geometry("400x550")
root.protocol("WM_DELETE_WINDOW", on_closing) #

# ID Inputs (Matching your specific database columns)
tk.Label(root, text="Consultant ID:").pack(pady=5)
entry_cons_id = tk.Entry(root); entry_cons_id.pack()

tk.Label(root, text="Customer ID:").pack(pady=5)
entry_cust_id = tk.Entry(root); entry_cust_id.pack()

# Calendar
tk.Label(root, text="Select Work Date:").pack(pady=5)
cal = DateEntry(root, width=12, background='darkblue', 
                foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
cal.pack(pady=5)

# Time Selectors (Spinboxes)
time_frame = tk.LabelFrame(root, text="Work Hours (24h format)", padx=10, pady=10)
time_frame.pack(pady=10)

tk.Label(time_frame, text="Start:").grid(row=0, column=0)
start_h = tk.Spinbox(time_frame, from_=0, to=23, width=3, format="%02.0f"); start_h.grid(row=0, column=1)
start_m = tk.Spinbox(time_frame, from_=0, to=59, width=3, format="%02.0f"); start_m.grid(row=0, column=2)

tk.Label(time_frame, text="End:").grid(row=1, column=0)
end_h = tk.Spinbox(time_frame, from_=0, to=23, width=3, format="%02.0f"); end_h.grid(row=1, column=1)
end_m = tk.Spinbox(time_frame, from_=0, to=59, width=3, format="%02.0f"); end_m.grid(row=1, column=2)

# Lunchbreak
var_lunch = tk.BooleanVar()
tk.Checkbutton(root, text="Lunch Break Included?", variable=var_lunch).pack(pady=10)

# Submit Button
btn_send = tk.Button(root, text="Log Hours to Azure", command=send_to_api, 
                     bg="#0078d4", fg="white", font=('Helvetica', 10, 'bold'))
btn_send.pack(pady=20)

root.mainloop()