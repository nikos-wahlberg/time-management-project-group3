# server/queries.py
from database import db
import psycopg2.extras

def fetch_dropdown_options():
    """
    Fetches both customers and consultants.
    """
    print("--- [DEBUG] Starting fetch_dropdown_options ---")
    data = {"consultants": [], "customers": []}
    
    with db.get_cursor() as cur:
        # 1. Get Consultants
        # print("--- [DEBUG] Executing SELECT for Consultants...")
        cur.execute("SELECT id, name FROM consultant ORDER BY name ASC;")
        
        raw_consultants = cur.fetchall()
        # print(f"--- [DEBUG] Raw Consultant Rows: {raw_consultants}")
        
        data["consultants"] = [{"id": row[0], "name": row[1]} for row in raw_consultants]

        # 2. Get Customers
        # print("--- [DEBUG] Executing SELECT for Customers...")
        cur.execute("SELECT id, name FROM customer ORDER BY name ASC;")
        
        raw_customers = cur.fetchall()
        # print(f"--- [DEBUG] Raw Customer Rows: {raw_customers}")
        
        data["customers"] = [{"id": row[0], "name": row[1]} for row in raw_customers]
        
    # print(f"--- [DEBUG] Final Data Structure to return: {data}")
    return data

def insert_worklog(consultant_id, customer_id, start_time, end_time, lunchbreak):
    """
    Inserts the worklog. 
    """
    print(f"--- [DEBUG] insert_worklog called with:")
    print(f"    Consultant: {consultant_id}, Customer: {customer_id}")
    print(f"    Start: {start_time}, End: {end_time}, Lunch: {lunchbreak}")

    sql = """
    INSERT INTO working_hours 
        (consultant_id, customer_id, start_time, end_time, lunchbreak)
    VALUES 
        (%s, %s, %s, %s, %s)
    RETURNING id;
    """
    
    with db.get_cursor() as cur:
        print("--- [DEBUG] Executing INSERT statement...")
        cur.execute(sql, (consultant_id, customer_id, start_time, end_time, lunchbreak))
        
        new_id = cur.fetchone()[0]
        print(f"--- [DEBUG] Success! New Record ID: {new_id}")
        return new_id


def insert_consultant(name):
    sql = "INSERT INTO consultant (name) VALUES (%s) RETURNING id;"
    with db.get_cursor() as cur:
        cur.execute(sql, (name,))
        return cur.fetchone()[0]

def insert_customer(name, max_hours):
    sql = "INSERT INTO customer (name, max_allocated_hours) VALUES (%s, %s) RETURNING id;"
    with db.get_cursor() as cur:
        cur.execute(sql, (name, max_hours))
        return cur.fetchone()[0]

def delete_consultant(id):
    """Deletes a consultant by ID."""
    sql = "DELETE FROM consultant WHERE id = %s;"
    with db.get_cursor() as cur:
        cur.execute(sql, (id,))
        # No return value needed, just execution

def delete_customer(id):
    """Deletes a customer by ID."""
    sql = "DELETE FROM customer WHERE id = %s;"
    with db.get_cursor() as cur:
        cur.execute(sql, (id,))