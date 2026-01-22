import pandas as pd
import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from sqlalchemy import create_engine
from io import StringIO
from key_vault import get_database_credentials

def get_db_engine():
    """Fetches credentials from Key Vault and creates a SQLAlchemy engine."""
    # Unpack all 12 variables returned by key_vault.py
    # Note: storage_account_name is returned twice in your key_vault script, 
    # so we use a throwaway variable '_' for the duplicate.
    host, database, user, password, port, blob_url, container_name, \
    resource_group, storage_acc, _, storage_connection, sub_id = get_database_credentials()
    
    # Construct the SQLAlchemy connection string with SSL required for Azure
    db_uri = f"postgresql://{user}:{password}@{host}:{port}/{database}?sslmode=require"
    return create_engine(db_uri)

def generate_report_content(df):
    try:
        buffer = StringIO()
        
        # Header
        buffer.write(f"CONSULTANT TIME REPORT\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        buffer.write("="*60 + "\n\n")

        # --- 1. DETAILED BREAKDOWN ---
        buffer.write("### 1. DETAILED BREAKDOWN (Consultant & Customer)\n")
        df['start_time'] = pd.to_datetime(df['start_time'])
        df['week'] = df['start_time'].dt.isocalendar().week
        
        detailed = df.groupby(['consultant_name', 'customer_name', 'week'])['total_time'].sum().reset_index()
        
        for _, row in detailed.iterrows():
            buffer.write(f"Week {row['week']} | {row['consultant_name']} @ {row['customer_name']}: {row['total_time']:.2f} hrs\n")
        buffer.write("\n")

        # --- 2. CUMULATIVE PROJECT HOURS ---
        buffer.write("### 2. CUMULATIVE PROJECT HOURS (By Customer)\n")
        customer_totals = df.groupby('customer_name')['total_time'].sum().reset_index()
        for _, row in customer_totals.iterrows():
            buffer.write(f"{row['customer_name']}: {row['total_time']:.2f} Total Hours\n")
        buffer.write("\n")

        # --- 3. CONSULTANT EFFICIENCY ---
        buffer.write("### 3. CONSULTANT EFFICIENCY (Avg Daily Hours)\n")
        df['date_only'] = df['start_time'].dt.date
        daily_sums = df.groupby(['consultant_name', 'date_only'])['total_time'].sum().reset_index()
        avg_daily = daily_sums.groupby('consultant_name')['total_time'].mean().reset_index()
        
        for _, row in avg_daily.iterrows():
            buffer.write(f"{row['consultant_name']}: {row['total_time']:.2f} hrs/day avg\n")

        return buffer.getvalue()
    except Exception as e:
        print(f"Error generating report content: {e}")
        return None

def run_report_process():
    try:
        # Fetch all info from Key Vault
        creds = get_database_credentials()
        if not creds:
            return False, "Failed to retrieve secrets from Key Vault."

        # Unpack for local use
        host, database, user, password, port, blob_url, container_name, \
        resource_group, storage_acc, _, storage_connection, sub_id = creds

        # 1. READ DATA FROM DB
        engine = get_db_engine()
        query = """
            SELECT 
                c.name as consultant_name,
                cust.name as customer_name,
                wh.start_time,
                wh.total_time
            FROM working_hours wh
            JOIN consultant c ON wh.consultant_id = c.id
            JOIN customer cust ON wh.customer_id = cust.id
        """
        
        with engine.connect() as connection:
            df = pd.read_sql(query, connection)

        if df.empty:
            return False, "No data found in database."

        # 2. GENERATE REPORT TEXT
        report_text = generate_report_content(df)

        # 3. UPLOAD TO AZURE BLOB STORAGE
        blob_service_client = BlobServiceClient.from_connection_string(storage_connection)
        container_client = blob_service_client.get_container_client(container_name)
        
        if not container_client.exists():
            container_client.create_container()

        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        blob_client = container_client.get_blob_client(filename)
        blob_client.upload_blob(report_text, overwrite=True)

        return True, filename

    except Exception as e:
        return False, str(e)

if __name__ == "__main__":    
    print("Generating report manually using Key Vault secrets...")
    success, message = run_report_process()
    if success:
        print(f"Success! Report uploaded as: {message}")
    else:
        print(f"Error: {message}")
        