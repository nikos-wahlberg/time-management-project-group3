import subprocess
import time
import os
import sys
import atexit

# 1. Define paths to your Server and Client scripts
# We use os.path.abspath to ensure it works regardless of where you run the command from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_SCRIPT = os.path.join(BASE_DIR, 'src', 'server', 'app.py')
CLIENT_SCRIPT = os.path.join(BASE_DIR, 'src', 'client', 'main.py')

# Global variable to hold the server process
server_process = None

def cleanup():
    """
    Kill the server when the app closes.
    """
    global server_process
    if server_process:
        print("Stopping Flask Server...")
        server_process.terminate() # or .kill() if it refuses to die
        server_process = None

# Register the cleanup function to run when this script exits
atexit.register(cleanup)

def main():
    global server_process

    print("--- 🚀 Starting Time Logger App ---")

    # 2. Start the Flask Server
    print(f"Starting Server from: {SERVER_SCRIPT}")
    try:
        # We pass 'python' (or sys.executable) to run the script
        server_process = subprocess.Popen(
            [sys.executable, SERVER_SCRIPT],
            cwd=os.path.dirname(SERVER_SCRIPT) # Run inside server folder
        )
    except Exception as e:
        print(f"CRITICAL ERROR: Could not start server: {e}")
        return

    # 3. Wait for Server to Initialize
    # Give Flask 2 seconds to connect to Azure and start listening
    print("Waiting for server to initialize...")
    time.sleep(3) 

    # 4. Start the Client (GUI)
    # We use .call() here so this script waits until the GUI is closed
    print(f"Starting Client from: {CLIENT_SCRIPT}")
    try:
        subprocess.call([sys.executable, CLIENT_SCRIPT])
    except Exception as e:
        print(f"Error running client: {e}")

    print("--- 👋 App Closed ---")
    # When this function ends, 'atexit' triggers cleanup() automatically

if __name__ == "__main__":
    main()