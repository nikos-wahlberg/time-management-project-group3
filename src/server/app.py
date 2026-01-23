# server/app.py
from flask import Flask, jsonify, request
from database import db
import logging
import re
from werkzeug.exceptions import HTTPException
from queries import (
    fetch_dropdown_options, insert_worklog, 
    insert_consultant, insert_customer,
    delete_consultant, delete_customer
    )

app = Flask(__name__)

with app.app_context():
    try:
        db.initialize()
    except Exception as e:
        print(f"Failed to connect to DB: {e}")

logging.basicConfig(
    filename='server_errors.log', 
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s'
)

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return jsonify({"error": e.description}), e.code

    logging.exception("An unhandled error occurred:")

    return jsonify({
        "error": "Internal Server Error",
        "details": str(e) 
    }), 500
    
@app.route('/api/options', methods=['GET'])
def get_options():
    """
    Endpoint for the GUI to fetch dropdown data.
    """
    try:
        data = fetch_dropdown_options()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/submit', methods=['POST'])
def submit_work():
    """
    Endpoint to save work hours.
    Expects JSON: {
        "consultant_id": 1,
        "customer_id": 2,
        "start_time": "2023-10-27 09:00:00",
        "end_time": "2023-10-27 17:00:00",
        "lunchbreak": true
    }
    """
    try:
        payload = request.json
        
        # Validate required fields
        required = ['consultant_id', 'customer_id', 'start_time', 'end_time', 'lunchbreak']
        if not all(k in payload for k in required):
            return jsonify({"error": "Missing required fields"}), 400

        # Call the logic layer
        record_id = insert_worklog(
            consultant_id=payload['consultant_id'],
            customer_id=payload['customer_id'],
            start_time=payload['start_time'],
            end_time=payload['end_time'],
            lunchbreak=payload.get('lunchbreak', False) 
        )
        
        return jsonify({"status": "success", "id": record_id}), 201

    except Exception as e:
        print(f"Error saving worklog: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/api/consultants', methods=['POST'])
def add_consultant_route():
    try:
        data = request.json
        if not data.get('name'):
            return jsonify({"error": "Name is required"}), 400
            
        new_id = insert_consultant(data['name'])
        
        return jsonify({
            "status": "success", 
            "id": new_id, 
            "message": f"Successfully added Consultant: {data['name']}"
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/customers', methods=['POST'])
def add_customer_route():
    try:
        data = request.json
        if not data.get('name'):
            return jsonify({"error": "Name is required"}), 400
            
        new_id = insert_customer(data['name'], data.get('max_allocated_hours', 0))
        
        return jsonify({
            "status": "success", 
            "id": new_id, 
            "message": f"Successfully added Customer: {data['name']}"
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/consultants/<int:id>', methods=['DELETE'])
def delete_consultant_route(id):
    try:
        delete_consultant(id)
        return jsonify({"status": "success", "message": f"Deleted Consultant ID: {id}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/customers/<int:id>', methods=['DELETE'])
def delete_customer_route(id):
    try:
        delete_customer(id)
        return jsonify({"status": "success", "message": f"Deleted Customer ID: {id}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# if __name__ == '__main__':
#     # Run on 0.0.0.0 to be accessible, port 5000 is standard
app.run(host='127.0.0.1', port=5000, debug=True)