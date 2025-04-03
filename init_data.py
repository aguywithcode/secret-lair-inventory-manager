#!/usr/bin/env python3

import sys
import os
import argparse

# Add the scripts directory to the path
script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
sys.path.append(script_dir)

# Import from the scripts directory
from initialize_data import initialize_data_directory

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Initialize MTG Inventory Manager data')
    parser.add_argument('--force', '-f', action='store_true', help='Force download even if recent file exists')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose debug output')
    args = parser.parse_args()
    
    sys.exit(0 if initialize_data_directory(args.verbose, args.force) else 1)
