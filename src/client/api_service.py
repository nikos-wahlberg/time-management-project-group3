import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError

BASE_URL = "http://127.0.0.1:5000/api"

def safe_request(method, endpoint, payload=None):
    """
    A generic wrapper to handle all network errors in one place.
    """
    url = f"{BASE_URL}/{endpoint}"
    
    response = None 

    try:
        if method == 'GET':
            response = requests.get(url, timeout=5)
        elif method == 'POST':
            response = requests.post(url, json=payload, timeout=5)
        elif method == 'DELETE': 
            response = requests.delete(url, timeout=5)
        else:
            return False, f"Method {method} not supported by client."

        response.raise_for_status()
        
        if response.content:
            return True, response.json()
        return True, {"message": "Success"}

    except ConnectionError:
        return False, "Could not reach the server. Is it running?"
    except Timeout:
        return False, "Request timed out. Server is slow."
    except HTTPError as e:
        error_msg = str(e)
        if response is not None:
            try:
                error_msg = response.json().get("error", str(e))
            except ValueError:
                pass 
        return False, f"Server Error: {error_msg}"
    except Exception as e:
        return False, f"Unexpected Error: {e}"

def fetch_options():
    success, result = safe_request('GET', 'options')
    if success:
        return result
    else:
        return {"error": result}

def add_new_consultant(name):
    """Sends a request to create a new consultant."""
    payload = {"name": name}
    success, result = safe_request('POST', 'consultants', payload)
    if success:
        return result
    else:
        return {"error": result}

def add_new_customer(name, max_hours):
    """Sends a request to create a new customer."""
    payload = {"name": name, "max_allocated_hours": max_hours}
    success, result = safe_request('POST', 'customers', payload)
    if success:
        return result
    else:
        return {"error": result}

def delete_consultant_by_id(id):
    """Sends a DELETE request for a specific consultant ID."""
    success, result = safe_request('DELETE', f'consultants/{id}')
    if success:
        return result
    else:
        return {"error": result}

def delete_customer_by_id(id):
    """Sends a DELETE request for a specific customer ID."""
    success, result = safe_request('DELETE', f'customers/{id}')
    if success:
        return result
    else:
        return {"error": result}
    


def submit_worklog(payload):
    success, result = safe_request('POST', 'submit', payload)
    if success:
        return result
    else:
        return {"error": result}