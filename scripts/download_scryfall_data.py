#!/usr/bin/env python3

import os
import requests
from tqdm import tqdm
import sys
import json
import time
import logging
import argparse
from datetime import datetime, timedelta

# Set up logger
logger = logging.getLogger(__name__)

def get_latest_all_cards_url():
    """
    Query the Scryfall Bulk Data API to get the URL for the latest all_cards data file
    
    Returns:
        str: URL of the latest all_cards file, or None if not found
    """
    logger.info("Fetching information about the latest Scryfall bulk data...")
    api_url = "https://api.scryfall.com/bulk-data"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        
        data = response.json()
        
        # Find the all_cards data object
        for item in data.get('data', []):
            if item.get('type') == 'all_cards':
                download_url = item.get('download_uri')
                logger.info(f"Found latest all_cards data (updated: {item.get('updated_at')})")
                logger.info(f"Size: {item.get('size') / (1024 * 1024):.2f} MB")
                return download_url
                
        logger.error("Could not find all_cards data in the Scryfall bulk data response")
        return None
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Scryfall bulk data information: {e}")
        return None

def is_file_recent(filepath, hours=24):
    """
    Check if a file exists and has been modified within the specified number of hours
    
    Args:
        filepath (str): Path to the file to check
        hours (int): Number of hours to consider "recent"
        
    Returns:
        bool: True if the file exists and is recent, False otherwise
    """
    if not os.path.exists(filepath):
        return False
        
    file_mtime = os.path.getmtime(filepath)
    file_time = datetime.fromtimestamp(file_mtime)
    current_time = datetime.now()
    
    # Check if the file was modified less than the specified hours ago
    time_diff = current_time - file_time
    if time_diff < timedelta(hours=hours):
        return True
    
    return False

def download_scryfall_data(url=None, directory="data", filename="scryfall_data.json"):
    """
    Download the bulk data from Scryfall and save it to the specified directory
    
    Args:
        url (str): The URL of the Scryfall bulk data, or None to fetch latest
        directory (str): The directory to save the file to
        filename (str): The name of the file to save the data as
    """
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Full path to the file
    filepath = os.path.join(directory, filename)
    
    # Check if the file already exists and is recent (within the last 24 hours)
    if is_file_recent(filepath):
        file_mtime = os.path.getmtime(filepath)
        file_time = datetime.fromtimestamp(file_mtime)
        logger.info(f"Scryfall data file already exists and is recent (last updated: {file_time.strftime('%Y-%m-%d %H:%M:%S')})")
        logger.info(f"Skipping download. Use --force flag to override.")
        return filepath
    
    # If no URL is provided, get the latest all_cards URL
    if not url:
        url = get_latest_all_cards_url()
        
    if not url:
        logger.error("No valid URL available for download")
        return None
    
    logger.info(f"Downloading Scryfall bulk data from: {url}")
    logger.info(f"This file will be saved to: {filepath}")
    
    try:
        # Make a streaming GET request
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Get the total file size in bytes
        total_size = int(response.headers.get('content-length', 0))
        
        # Download the file with progress bar
        with open(filepath, 'wb') as file, tqdm(
            desc=filename,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            disable=logger.level > logging.INFO  # Only show progress bar if not in debug mode
        ) as progress_bar:
            for data in response.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                file.write(data)
                progress_bar.update(len(data))
        
        logger.info(f"Download complete! File saved to {filepath}")
        return filepath
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading file: {e}")
        return None

def setup_logging(verbose=False):
    """Configure logging based on verbosity level"""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # Set third-party loggers to a higher level to reduce noise
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Download Scryfall bulk card data')
    parser.add_argument('url', nargs='?', help='Optional URL to download from (if not provided, uses Scryfall API)')
    parser.add_argument('--force', '-f', action='store_true', help='Force download even if recent file exists')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose debug output')
    args = parser.parse_args()
    
    # Set up logging based on verbosity
    setup_logging(args.verbose)
    
    # If force flag is specified, delete the existing file if it exists
    if args.force:
        filepath = os.path.join("data", "scryfall_data.json")
        if os.path.exists(filepath):
            logger.info(f"Force flag specified, removing existing file {filepath}")
            os.remove(filepath)
    
    download_scryfall_data(args.url)