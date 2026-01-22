import json
import psycopg2
from flask import Flask, request, jsonify
from key_vault import get_database_credentials

app = Flask(__name__)

def get_db_connection():
    try:
        host, database, user, password, *_ = get_database_credentials()
        return psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password, 
            sslmode="require"
        )
    except Exception as e:
        print(e)


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

if __name__ == '__main__':
    app.run(debug=True)