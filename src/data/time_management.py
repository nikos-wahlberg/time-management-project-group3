import json
import psycopg2
from flask import Flask, request, jsonify
from key_vault import get_database_credentials
<<<<<<< HEAD
app = Flask(__name__)

#with open('config.json', 'r') as f:
#    config_data = json.load(f)
#    azure_config = config_data['azure']

db_credentials = get_database_credentials()

def get_db_connection():
    # host, database, user, passport, port = get_database_credentials()
    return psycopg2.connect(
        host=db_credentials['host'],
        database=db_credentials['database'],
        user=db_credentials['user'],
        password=db_credentials['password'], 
        sslmode="require"
    )
=======
# from key_vault import get_database_credentials
from reporting import run_report_process

app = Flask(__name__)

# with open('config.json', 'r') as f:
#     config_data = json.load(f)
#     azure_config = config_data['azure']

def get_db_connection():
    try:
        host, database, user, password, port = get_database_credentials()
        return psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password, 
            sslmode="require"
        )
    except Exception as e:
        print(e)

# def get_db_connection():
#     host, database, user, passport, port = get_database_credentials()
#     return psycopg2.connect(
#         host=azure_config['host'],
#         database=azure_config['database'],
#         user=azure_config['user'],
#         password=azure_config['password'], 
#         sslmode="require"
#     )
>>>>>>> d56e834c0d8f9b93a4cfc6aa7a9f5e9959fb740e

@app.route('/add-hours', methods=['POST'])
def add_hours():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO working_hours(start_time, end_time, lunchbreak, consultant_id, customer_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            data['start_time'], 
            data['end_time'], 
            data['lunchbreak'], 
            data['consultant_id'], 
            data['customer_id']
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "message": "Logged to Azure!"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Reporting endpoint
@app.route('/report', methods=['POST'])
def trigger_report():
    try:
        success, result = run_report_process()
        
        if success:
            return jsonify({
                "status": "success", 
                "message": "Report generated and uploaded.", 
                "filename": result
            }), 200
        else:
            return jsonify({
                "status": "error", 
                "message": result
            }), 500
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)