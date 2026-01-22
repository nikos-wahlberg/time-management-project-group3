import os
import sys
import subprocess
import time
import atexit
from main_window import TimeLoggerApp

# Global variable to track the server process
server_process = None

def start_server():
    """
    Locates and starts the Flask server as a subprocess.
    """
    global server_process
    
    # 1. Calculate path to server/app.py relative to this file
    # client/main.py -> up one level -> server -> app.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir) # Go up to 'src'
    server_script = os.path.join(project_root, 'server', 'app.py')

    print(f"--- Launching Server: {server_script} ---")

    try:
        # 2. Start the process non-blocking (Popen)
        # We set the cwd (current working directory) to the server folder
        # so it can find 'database.py' and 'key_vault.py' easily.
        server_process = subprocess.Popen(
            [sys.executable, server_script],
            cwd=os.path.dirname(server_script)
        )
        
        # 3. Give it a moment to connect to Azure/Database
        print("Waiting 2 seconds for server startup...")
        time.sleep(2)
        
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to start server: {e}")

def cleanup_server():
    """
    Kills the server process when the GUI closes.
    """
    global server_process
    if server_process:
        print("--- Closing App: Terminating Server ---")
        server_process.terminate()
        server_process = None

# Register the cleanup function to run automatically when Python exits
atexit.register(cleanup_server)

if __name__ == "__main__":
    # 1. Start the backend
    start_server()

    # 2. Start the frontend
    try:
        app = TimeLoggerApp()
        app.mainloop()
    except Exception as e:
        print(f"GUI Error: {e}")
    
    # The atexit handler will trigger here automatically