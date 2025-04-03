#!/usr/bin/env python3

import sys
import os

# Add the scripts directory to the path
script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
sys.path.append(script_dir)

# Import from the scripts directory
from initialize_data import initialize_data_directory

if __name__ == "__main__":
    sys.exit(0 if initialize_data_directory() else 1)
