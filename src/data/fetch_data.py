from tkinter import messagebox
from connect import get_database_connection

def fetch_dropdown_data():
    """
    Connects to Azure PostgreSQL, fetches names/IDs, and returns dictionaries.
    """

    cons_map = {} 
    cust_map = {}

    try:
        # Connect to PostgreSQL
        conn = get_database_connection()
        cursor = conn.cursor()

        # 1. Fetch Consultants (Adjust table/column names if needed)
        # Assuming table is 'consultants' and columns are 'id', 'name'
        cursor.execute("SELECT id, name FROM consultants") 
        for row in cursor.fetchall():
            cons_map[row[1]] = row[0] # { "John Doe": 1 }

        # 2. Fetch Customers
        # Assuming table is 'customers' and columns are 'id', 'company_name'
        cursor.execute("SELECT id, company_name FROM customers")
        for row in cursor.fetchall():
            cust_map[row[1]] = row[0] # { "Acme Corp": 5 }

        conn.close()
        return cons_map, cust_map

    except Exception as e:
        print(f"PostgreSQL Error: {e}")
        messagebox.showerror("Database Error", f"Failed to fetch data:\n{e}")
        return {}, {}