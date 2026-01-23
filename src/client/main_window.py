import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry
import api_service

class TimeLoggerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Azure Time Management System")
        self.geometry("450x600")
        
        # Data Storage
        self.consultant_map = {}
        self.customer_map = {}

        # --- 1. Create Tabs Container ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', pady=10)

        # --- 2. Create the Frames for each Tab ---
        self.tab_log = ttk.Frame(self.notebook)
        self.tab_add_consultant = ttk.Frame(self.notebook)
        self.tab_add_customer = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_log, text='Log Hours')
        self.notebook.add(self.tab_add_consultant, text='Add Consultant')
        self.notebook.add(self.tab_add_customer, text='Add Customer')

        # --- 3. Build Widgets for each Tab ---
        self.setup_log_tab()
        self.setup_consultant_tab()
        self.setup_customer_tab()

        # --- 4. Load Data ---
        self.load_data()

    def setup_log_tab(self):
        """Builds the Log Hours interface with Start/End time inputs"""
        frame = self.tab_log
        
        # --- Consultant Selection ---
        ttk.Label(frame, text="Select Consultant:").pack(pady=(20, 5))
        self.consultant_var = tk.StringVar()
        self.consultant_combo = ttk.Combobox(frame, textvariable=self.consultant_var, state="readonly", width=30)
        self.consultant_combo.pack(pady=5) 

        # --- Customer Selection ---
        ttk.Label(frame, text="Select Customer:").pack(pady=(10, 5))
        self.customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(frame, textvariable=self.customer_var, state="readonly", width=30)
        self.customer_combo.pack(pady=5)

        # --- Date Entry ---
        ttk.Label(frame, text="Select Work Date:").pack(pady=(10, 5))
        self.date_entry = DateEntry(frame, width=12, background='darkblue', 
                                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.pack(pady=5)

        # --- Time Frame Selection ---
        time_frame = ttk.LabelFrame(frame, text="Work Hours (24h format)", padding=(10, 10))
        time_frame.pack(pady=10)

        # Start Time
        ttk.Label(time_frame, text="Start:").grid(row=0, column=0, padx=5)
        
        # 1. Create Variables for Start Time
        self.var_start_h = tk.StringVar(value="09") 
        self.var_start_m = tk.StringVar(value="00") 

        # 2. Bind them to the Spinboxes using 'textvariable'
        tk.Spinbox(time_frame, from_=0, to=23, width=3, format="%02.0f", wrap=True, textvariable=self.var_start_h).grid(row=0, column=1)
        ttk.Label(time_frame, text=":").grid(row=0, column=2)
        tk.Spinbox(time_frame, from_=0, to=59, width=3, format="%02.0f", wrap=True, textvariable=self.var_start_m).grid(row=0, column=3)

        # End Time
        ttk.Label(time_frame, text="End:").grid(row=1, column=0, padx=5, pady=5)
        
        # 3. Create Variables for End Time
        self.var_end_h = tk.StringVar(value="17") 
        self.var_end_m = tk.StringVar(value="00") 
        
        tk.Spinbox(time_frame, from_=0, to=23, width=3, format="%02.0f", wrap=True, textvariable=self.var_end_h).grid(row=1, column=1, pady=5)
        ttk.Label(time_frame, text=":").grid(row=1, column=2)
        tk.Spinbox(time_frame, from_=0, to=59, width=3, format="%02.0f", wrap=True, textvariable=self.var_end_m).grid(row=1, column=3, pady=5)

        # --- Lunch Break ---
        self.lunch_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Lunch Break (30 min)?", variable=self.lunch_var).pack(pady=10)

        # --- Buttons ---
        self.submit_btn = ttk.Button(frame, text="Submit Log", command=self.submit_worklog)
        self.submit_btn.pack(pady=10)
        
        ttk.Button(frame, text="🔄 Refresh Data", command=self.load_data).pack(pady=5)

    def setup_consultant_tab(self):
        """Builds the interface to Add OR Delete a consultant"""
        frame = self.tab_add_consultant
        
        # --- SECTION: CREATE ---
        ttk.Label(frame, text="Create New Consultant", font=("Helvetica", 12, "bold")).pack(pady=(20, 10))
        
        ttk.Label(frame, text="Full Name:").pack(pady=5)
        self.new_cons_name = tk.StringVar()
        ttk.Entry(frame, textvariable=self.new_cons_name, width=30).pack(pady=5)
        
        ttk.Button(frame, text="Create Consultant", command=self.submit_new_consultant).pack(pady=10)

        # --- SEPARATOR ---
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=20, padx=20)

        # --- SECTION: DELETE ---
        ttk.Label(frame, text="Delete Existing Consultant", font=("Helvetica", 12, "bold"), foreground="red").pack(pady=10)
        
        ttk.Label(frame, text="Select to Delete:").pack(pady=5)
        self.del_cons_var = tk.StringVar()
        self.del_cons_combo = ttk.Combobox(frame, textvariable=self.del_cons_var, state="readonly", width=30)
        self.del_cons_combo.pack(pady=5)

        ttk.Button(frame, text="❌ Delete Selected", command=self.submit_delete_consultant).pack(pady=10)

    def setup_customer_tab(self):
        """Builds the interface to Add OR Delete a customer"""
        frame = self.tab_add_customer
        
        # --- SECTION: CREATE ---
        ttk.Label(frame, text="Create New Customer", font=("Helvetica", 12, "bold")).pack(pady=(20, 10))
        
        ttk.Label(frame, text="Company Name:").pack(pady=5)
        self.new_cust_name = tk.StringVar()
        ttk.Entry(frame, textvariable=self.new_cust_name, width=30).pack(pady=5)

        ttk.Label(frame, text="Max Allocated Hours:").pack(pady=5)
        self.new_cust_hours = tk.StringVar()
        ttk.Entry(frame, textvariable=self.new_cust_hours, width=30).pack(pady=5)
        
        ttk.Button(frame, text="Create Customer", command=self.submit_new_customer).pack(pady=10)

        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=20, padx=20)

        ttk.Label(frame, text="Delete Existing Customer", font=("Helvetica", 12, "bold"), foreground="red").pack(pady=10)
        
        ttk.Label(frame, text="Select to Delete:").pack(pady=5)
        self.del_cust_var = tk.StringVar()
        self.del_cust_combo = ttk.Combobox(frame, textvariable=self.del_cust_var, state="readonly", width=30)
        self.del_cust_combo.pack(pady=5)

        ttk.Button(frame, text="❌ Delete Selected", command=self.submit_delete_customer).pack(pady=10)

    def load_data(self):
        """Fetches data and populates ALL dropdowns in the app"""
        self.submit_btn.config(state="disabled") 
        
        data = api_service.fetch_options()
        if not data or "error" in data:
            if data: messagebox.showerror("Error", data["error"])
            return

        self.consultant_map = {c['name']: c['id'] for c in data.get('consultants', [])}
        self.customer_map = {c['name']: c['id'] for c in data.get('customers', [])}
        
        cons_list = list(self.consultant_map.keys())
        cust_list = list(self.customer_map.keys())
        
        self.consultant_combo['values'] = cons_list
        self.customer_combo['values'] = cust_list

        self.del_cons_combo['values'] = cons_list
        self.del_cust_combo['values'] = cust_list

        self.submit_btn.config(state="normal") 

    def submit_worklog(self):
        cons_name = self.consultant_var.get()
        cust_name = self.customer_var.get()
        
        date_str = self.date_entry.get_date()
        if isinstance(date_str, type(datetime.now().date())):
            date_str = date_str.strftime("%Y-%m-%d")
        else:
            date_str = str(date_str)

        if not all([cons_name, cust_name]):
            messagebox.showwarning("Missing Data", "Please select a Consultant and Customer.")
            return

        try:
            sh = f"{int(self.var_start_h.get()):02d}"
            sm = f"{int(self.var_start_m.get()):02d}"
            eh = f"{int(self.var_end_h.get()):02d}"
            em = f"{int(self.var_end_m.get()):02d}"

            start_dt_str = f"{date_str} {sh}:{sm}:00"
            end_dt_str = f"{date_str} {eh}:{em}:00"

            start_dt = datetime.strptime(start_dt_str, "%Y-%m-%d %H:%M:%S")
            end_dt = datetime.strptime(end_dt_str, "%Y-%m-%d %H:%M:%S")

            if start_dt > datetime.now():
                messagebox.showerror("Date Error", "You cannot submit work hours for a future date/time.")
                return
            
            if end_dt > datetime.now():
                messagebox.showerror("Time Error", "You cannot log hours that haven't occurred yet.")
                return

            if end_dt <= start_dt:
                messagebox.showerror("Time Error", "End time must be after Start time.")
                return
  

            payload = {
                "consultant_id": self.consultant_map[cons_name],
                "customer_id": self.customer_map[cust_name],
                "start_time": start_dt_str,
                "end_time": end_dt_str,
                "lunchbreak": self.lunch_var.get()
            }

            result = api_service.submit_worklog(payload)
            
            if "error" in result:
                messagebox.showerror("Server Error", result["error"])
            else:
                messagebox.showinfo("Success", "Worklog saved successfully!")
                self.var_start_h.set("09")
                self.var_start_m.set("00")
                self.var_end_h.set("17")
                self.var_end_m.set("00")

        except ValueError:
            messagebox.showerror("Input Error", "Invalid time values entered.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def submit_new_consultant(self):
        name = self.new_cons_name.get()
        if not name:
            messagebox.showwarning("Input Error", "Name is required")
            return
            
        result = api_service.add_new_consultant(name)
        if "error" in result:
            messagebox.showerror("Error", result["error"])
        else:
            messagebox.showinfo("Success", result["message"])
            self.new_cons_name.set("") 
            self.load_data() 

    def submit_new_customer(self):
        name = self.new_cust_name.get()
        hours = self.new_cust_hours.get()
        if not name:
            messagebox.showwarning("Input Error", "Name is required")
            return
            
        if not hours: hours = "0"
            
        result = api_service.add_new_customer(name, int(hours))
        if "error" in result:
            messagebox.showerror("Error", result["error"])
        else:
            messagebox.showinfo("Success", result["message"])
            self.new_cust_name.set("")
            self.new_cust_hours.set("")
            self.load_data() 

    def submit_delete_consultant(self):
        name = self.del_cons_var.get()
        if not name:
            messagebox.showwarning("Selection Error", "Please select a consultant to delete.")
            return
            
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'?\nThis cannot be undone.")
        if not confirm:
            return

        cons_id = self.consultant_map[name]
        result = api_service.delete_consultant_by_id(cons_id)

        if "error" in result:
            messagebox.showerror("Error", result["error"])
        else:
            messagebox.showinfo("Success", f"Deleted Consultant: {name}")
            self.del_cons_var.set("") 
            self.load_data() 

    def submit_delete_customer(self):
        name = self.del_cust_var.get()
        if not name:
            messagebox.showwarning("Selection Error", "Please select a customer to delete.")
            return
            
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'?")
        if not confirm:
            return

        cust_id = self.customer_map[name]
        result = api_service.delete_customer_by_id(cust_id)

        if "error" in result:
            messagebox.showerror("Error", result["error"])
        else:
            messagebox.showinfo("Success", f"Deleted Customer: {name}")
            self.del_cust_var.set("")
            self.load_data()

