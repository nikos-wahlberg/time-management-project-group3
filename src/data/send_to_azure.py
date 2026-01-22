import tkinter as tk
import tkinter.ttk as ttk  # Required for Tabs
from tkinter import messagebox
from tkcalendar import DateEntry
import subprocess
import time
import requests
import os


# --- API FUNCTION 1: LOG HOURS (Existing) ---
def send_working_hours(cal, start_h, start_m, end_h, end_m, entry_cons_id, entry_cust_id, var_lunch):
    selected_date = cal.get_date()
    start_dt = f"{selected_date} {start_h.get()}:{start_m.get()}:00"
    end_dt = f"{selected_date} {end_h.get()}:{end_m.get()}:00"

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
            messagebox.showerror("Error", f"Server returned: {response.status_code}\n{response.text}")
    except Exception as e:
        messagebox.showerror("Connection Error", "Is the Flask server running?")

# --- API FUNCTION 2: ADD CONSULTANT (New) ---
def send_new_consultant(entry_name):
    name = entry_name.get()
    if not name:
        messagebox.showwarning("Input Error", "Please enter a name.")
        return

    url = "http://127.0.0.1:5000/add-consultant"
    try:
        response = requests.post(url, json={"name": name})
        if response.status_code == 201:
            # The backend returns the new ID, so we show it to the user
            new_id = response.json().get('message') 
            messagebox.showinfo("Success", new_id) 
            entry_name.delete(0, 'end') # Clear input
        else:
            messagebox.showerror("Error", f"Server: {response.text}")
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))

# --- API FUNCTION 3: ADD CUSTOMER (New) ---
def send_new_customer(entry_name, entry_hours):
    name = entry_name.get()
    hours = entry_hours.get()
    
    if not name:
        messagebox.showwarning("Input Error", "Customer name is required.")
        return

    url = "http://127.0.0.1:5000/add-customer"
    try:
        # Send max_hours only if provided, otherwise send empty string (backend handles it)
        payload = {"name": name, "max_allocated_hours": hours if hours else ""}
        response = requests.post(url, json=payload)
        if response.status_code == 201:
            new_id = response.json().get('message')
            messagebox.showinfo("Success", new_id)
            entry_name.delete(0, 'end') 
            entry_hours.delete(0, 'end')
        else:
            messagebox.showerror("Error", f"Server: {response.text}")
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))