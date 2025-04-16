#!/usr/bin/env python3

import os
import sys
import argparse

def run_web_ui(host='127.0.0.1', port=5000, debug=False):
    """
    Start the web UI server
    
    Args:
        host (str): Host to bind to
        port (int): Port to bind to
        debug (bool): Whether to run in debug mode
    """
    # Add the project root to the path
    web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web')
    sys.path.append(web_dir)
    
    # Import the Flask app
    try:
        from web.app import app
        print(f"Starting MTG Inventory Manager Web UI at http://{host}:{port}")
        app.run(host=host, port=port, debug=debug)
    except ImportError as e:
        print(f"Error importing Flask app: {e}")
        print("Make sure you have installed Flask and other requirements:")
        print("pip install -r requirements.txt")
        return 1
    
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the MTG Inventory Manager Web UI")
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    sys.exit(run_web_ui(args.host, args.port, args.debug))
