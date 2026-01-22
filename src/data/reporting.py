import pandas as pd
import json
import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from sqlalchemy import create_engine
from io import StringIO
from key_vault import get_database_credentials

# Load Configuration
def load_config():
    # Ensure we are looking for config.json in the same directory as this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, 'config.json')
    
    with open(config_path, 'r') as f:
        return json.load(f)['azure']

def get_database_engine():
    # Construct the SQLAlchemy connection string
    # Format: postgresql://user:password@host:port/database
    host, database, user, password, port = get_database_credentials()
    db_uri = f"postgresql://{user}:{password}@{host}:5432/{database}"
    return create_engine(db_uri)

def generate_report_content(df):
    try:
        buffer = StringIO()
        
        # Header
        buffer.write(f"CONSULTANT TIME REPORT\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        buffer.write("="*60 + "\n\n")

        # --- 1. Daily/Weekly Total by Consultant & Customer ---
        buffer.write("### 1. DETAILED BREAKDOWN (Consultant & Customer)\n")
        # Ensure start_time is datetime
        df['start_time'] = pd.to_datetime(df['start_time'])
        
        # Calculate week number
        df['week'] = df['start_time'].dt.isocalendar().week
        
        detailed = df.groupby(['consultant_name', 'customer_name', 'week'])['total_time'].sum().reset_index()
        
        for _, row in detailed.iterrows():
            buffer.write(f"Week {row['week']} | {row['consultant_name']} @ {row['customer_name']}: {row['total_time']:.2f} hrs\n")
        buffer.write("\n")

        # --- 2. Cumulative Hours by Customer (All Consultants) ---
        buffer.write("### 2. CUMULATIVE PROJECT HOURS (By Customer)\n")
        customer_totals = df.groupby('customer_name')['total_time'].sum().reset_index()
        for _, row in customer_totals.iterrows():
            buffer.write(f"{row['customer_name']}: {row['total_time']:.2f} Total Hours\n")
        buffer.write("\n")

        # --- 3. Average Daily Working Hours per Consultant ---
        buffer.write("### 3. CONSULTANT EFFICIENCY (Avg Daily Hours)\n")
        df['date_only'] = df['start_time'].dt.date
        daily_sums = df.groupby(['consultant_name', 'date_only'])['total_time'].sum().reset_index()
        avg_daily = daily_sums.groupby('consultant_name')['total_time'].mean().reset_index()
        
        for _, row in avg_daily.iterrows():
            buffer.write(f"{row['consultant_name']}: {row['total_time']:.2f} hrs/day avg\n")

        return buffer.getvalue()
    except Exception as e:
        print(e)

def run_report_process():
    try:
        config = load_config()
        
        # 1. READ DATA FROM DB (Using SQLAlchemy Engine)
        engine = get_database_engine(config)
        
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
        
        # Use a context manager to ensure connection closes
        with engine.connect() as connection:
            df = pd.read_sql(query, connection)

        if df.empty:
            return False, "No data found in database."

        # 2. GENERATE REPORT TEXT
        report_text = generate_report_content(df)

        # 3. UPLOAD TO AZURE BLOB STORAGE
        blob_service_client = BlobServiceClient.from_connection_string(config['storage_connection_string'])
        container_client = blob_service_client.get_container_client(config['container_name'])
        
        if not container_client.exists():
            container_client.create_container()

        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        blob_client = container_client.get_blob_client(filename)
        blob_client.upload_blob(report_text, overwrite=True)

        return True, filename

    except KeyError as e:
        return False, f"Missing key in config.json: {e}"
    except Exception as e:
        return False, str(e)
# Reporting endpoint
# @app.route('/report', methods=['POST'])
# def trigger_report():
#     try:
#         success, result = run_report_process()
        
#         if success:
#             return jsonify({
#                 "status": "success", 
#                 "message": "Report generated and uploaded.", 
#                 "filename": result
#             }), 200
#         else:
#             return jsonify({
#                 "status": "error", 
#                 "message": result
#             }), 500
            
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500


# --- CLI ENTRY POINT ---
if __name__ == "__main__":    
    print("Generating report manually...")
    success, message = run_report_process()
    if success:
        print(f"Success! Report uploaded as: {message}")
    else:
        print(f"Error: {message}")