#!/usr/bin/env python3

import os
import sys
import time
import logging
import argparse
# Update imports to use fully qualified paths
from scripts.download_scryfall_data import download_scryfall_data, setup_logging
from scripts.scrape_secret_lairs import scrape_secret_lairs, save_to_json

# Set up logger
logger = logging.getLogger(__name__)

def initialize_data_directory(verbose=False, force=False):
    """
    Initialize the data directory by downloading Scryfall data and scraping Secret Lair information.
    This creates all the necessary data files for the MTG Inventory Manager.
    
    Args:
        verbose (bool): Whether to show verbose debug output
        force (bool): Whether to force download even if recent file exists
    """
    # Configure logging based on verbosity
    setup_logging(verbose)
    
    logger.info("=" * 60)
    logger.info("MTG INVENTORY MANAGER - DATA INITIALIZATION")
    logger.info("=" * 60)
    
    # Create data directory if it doesn't exist
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    success = True
    
    # Step 1: Download Scryfall bulk data
    logger.info("\n[Step 1/2] Downloading Scryfall card data")
    logger.info("-" * 60)
    start_time = time.time()
    try:
        # If force flag is specified and the file exists, delete it
        if force:
            filepath = os.path.join(data_dir, "scryfall_data.json")
            if os.path.exists(filepath):
                logger.info(f"Force flag specified, removing existing file {filepath}")
                os.remove(filepath)
        
        scryfall_file = download_scryfall_data(directory=data_dir)
        if not scryfall_file:
            logger.warning("Failed to download Scryfall data")
            success = False
    except Exception as e:
        logger.error(f"Exception occurred while downloading Scryfall data: {e}", exc_info=verbose)
        success = False
    
    elapsed_time = time.time() - start_time
    logger.info(f"Scryfall download completed in {elapsed_time:.1f} seconds")
    
    # Step 2: Scrape Secret Lair data
    logger.info("\n[Step 2/2] Scraping Secret Lair data")
    logger.info("-" * 60)
    start_time = time.time()
    try:
        # Use the match_with_scryfall option to add card details from Scryfall
        secret_lairs = scrape_secret_lairs(match_with_scryfall=True, 
                                           scryfall_filepath=os.path.join(data_dir, "scryfall_data.json"))
        if secret_lairs:
            save_to_json(secret_lairs, directory=data_dir)
        else:
            logger.warning("Failed to scrape Secret Lair data")
            success = False
    except Exception as e:
        logger.error(f"Exception occurred while scraping Secret Lair data: {e}", exc_info=verbose)
        success = False
    
    elapsed_time = time.time() - start_time
    logger.info(f"Secret Lair scraping completed in {elapsed_time:.1f} seconds")
    
    # Final status
    logger.info("\n" + "=" * 60)
    if success:
        logger.info("Data initialization COMPLETED SUCCESSFULLY")
        logger.info(f"All data files have been saved to the '{data_dir}' directory")
    else:
        logger.warning("Data initialization COMPLETED WITH WARNINGS")
        logger.warning("Some data files may be missing or incomplete")
    logger.info("=" * 60)
    
    return success

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Initialize MTG Inventory Manager data')
    parser.add_argument('--force', '-f', action='store_true', help='Force download even if recent file exists')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose debug output')
    args = parser.parse_args()
    
    sys.exit(0 if initialize_data_directory(args.verbose, args.force) else 1)