#!/usr/bin/env python3

import os
import sys
import argparse
import errno # Added for EADDRINUSE

def run_web_ui(host='127.0.0.1', port=5000, debug=False):
    """
    Start the web UI server, trying alternative ports if the default is in use.
    
    Args:
        host (str): Host to bind to
        port (int): Initial port to try
        debug (bool): Whether to run in debug mode
    """
    # Add the project root to the path
    web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web')
    sys.path.append(web_dir)
    
    try:
        from web.app import app
    except ImportError as e:
        print(f"Error importing Flask app: {e}")
        print("Make sure you have installed Flask and other requirements:")
        print("pip install -r requirements.txt")
        return 1

    current_port = port
    max_retries = 10  # Try up to 10 ports (e.g., 5000 to 5009)
    for i in range(max_retries):
        try:
            print(f"Attempting to start MTG Inventory Manager Web UI at http://{host}:{current_port}")
            # The app.run() call is blocking, so if it succeeds, this function effectively stops here
            # until the server is shut down.
            app.run(host=host, port=current_port, debug=debug)
            # If app.run() returns (e.g. server was shut down), we consider it a success for this port.
            return 0 
        except OSError as e:
            if e.errno == errno.EADDRINUSE:
                print(f"Port {current_port} is already in use.")
                current_port += 1
                if i < max_retries - 1:
                    print(f"Trying port {current_port}...")
                else:
                    print("Maximum number of port retries reached.")
            else:
                # Other OS error
                print(f"An OS error occurred: {e}")
                return 1
        except Exception as e:
            # Catch any other unexpected errors during app.run()
            print(f"An unexpected error occurred: {e}")
            return 1
            
    print(f"Failed to start the web UI after trying ports {port} to {current_port -1}.")
    return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the MTG Inventory Manager Web UI")
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    sys.exit(run_web_ui(args.host, args.port, args.debug))
