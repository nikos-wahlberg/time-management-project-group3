from database import db

def fetch_dropdown_options():
    """
    Fetches both customers and consultants.
    """
    data = {"consultants": [], "customers": []}
    
    with db.get_cursor() as cur:
        cur.execute("SELECT id, name FROM consultant ORDER BY name ASC;")
        raw_consultants = cur.fetchall()
        data["consultants"] = [{"id": row[0], "name": row[1]} for row in raw_consultants]

        cur.execute("SELECT id, name FROM customer ORDER BY name ASC;")
        raw_customers = cur.fetchall()
        data["customers"] = [{"id": row[0], "name": row[1]} for row in raw_customers]
        
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
        cur.execute(sql, (consultant_id, customer_id, start_time, end_time, lunchbreak))
        
        new_id = cur.fetchone()[0]
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

def delete_customer(id):
    """Deletes a customer by ID."""
    sql = "DELETE FROM customer WHERE id = %s;"
    with db.get_cursor() as cur:
        cur.execute(sql, (id,))