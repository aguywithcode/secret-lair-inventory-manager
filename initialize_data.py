#!/usr/bin/env python3

import os
import sys
import time
from download_scryfall_data import download_scryfall_data
from scrape_secret_lairs import scrape_secret_lairs, save_to_json

def initialize_data_directory():
    """
    Initialize the data directory by downloading Scryfall data and scraping Secret Lair information.
    This creates all the necessary data files for the MTG Inventory Manager.
    """
    print("=" * 60)
    print("MTG INVENTORY MANAGER - DATA INITIALIZATION")
    print("=" * 60)
    
    # Create data directory if it doesn't exist
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    success = True
    
    # Step 1: Download Scryfall bulk data
    print("\n[Step 1/2] Downloading Scryfall card data")
    print("-" * 60)
    start_time = time.time()
    try:
        scryfall_file = download_scryfall_data(directory=data_dir)
        if not scryfall_file:
            print("WARNING: Failed to download Scryfall data")
            success = False
    except Exception as e:
        print(f"ERROR: Exception occurred while downloading Scryfall data: {e}")
        success = False
    
    elapsed_time = time.time() - start_time
    print(f"Scryfall download completed in {elapsed_time:.1f} seconds")
    
    # Step 2: Scrape Secret Lair data
    print("\n[Step 2/2] Scraping Secret Lair data")
    print("-" * 60)
    start_time = time.time()
    try:
        # Use the match_with_scryfall option to add card details from Scryfall
        secret_lairs = scrape_secret_lairs(match_with_scryfall=True, 
                                          scryfall_filepath=os.path.join(data_dir, "scryfall_data.json"))
        if secret_lairs:
            save_to_json(secret_lairs, directory=data_dir)
        else:
            print("WARNING: Failed to scrape Secret Lair data")
            success = False
    except Exception as e:
        print(f"ERROR: Exception occurred while scraping Secret Lair data: {e}")
        success = False
    
    elapsed_time = time.time() - start_time
    print(f"Secret Lair scraping completed in {elapsed_time:.1f} seconds")
    
    # Final status
    print("\n" + "=" * 60)
    if success:
        print("Data initialization COMPLETED SUCCESSFULLY")
        print(f"All data files have been saved to the '{data_dir}' directory")
    else:
        print("Data initialization COMPLETED WITH WARNINGS")
        print("Some data files may be missing or incomplete")
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    sys.exit(0 if initialize_data_directory() else 1)
