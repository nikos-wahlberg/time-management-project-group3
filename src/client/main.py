import os
import sys
import subprocess
import time
import atexit
from main_window import TimeLoggerApp

server_process = None

def start_server():
    """
    Locates and starts the Flask server as a subprocess.
    """
    global server_process
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir) 
    server_script = os.path.join(project_root, 'server', 'app.py')

    print(f"--- Launching Server: ---")

    try:
        server_process = subprocess.Popen(
            [sys.executable, server_script],
            cwd=os.path.dirname(server_script),
            stdout=subprocess.DEVNULL,  
            stderr=subprocess.STDOUT
        )
        
        time.sleep(3)
        
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

atexit.register(cleanup_server)

if __name__ == "__main__":
    start_server()

    try:
        app = TimeLoggerApp()
        app.mainloop()
    except Exception as e:
        print(f"GUI Error: {e}")
    