#!/usr/bin/env python3

import os
import requests
from tqdm import tqdm
import sys

def download_scryfall_data(url, directory="data"):
    """
    Download the bulk data from Scryfall and save it to the specified directory
    
    Args:
        url (str): The URL of the Scryfall bulk data
        directory (str): The directory to save the file to
    """
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Extract filename from URL
    filename = url.split("/")[-1]
    filepath = os.path.join(directory, filename)
    
    print(f"Downloading Scryfall bulk data from: {url}")
    print(f"This file will be saved to: {filepath}")
    
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
        ) as progress_bar:
            for data in response.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                file.write(data)
                progress_bar.update(len(data))
        
        print(f"Download complete! File saved to {filepath}")
        return filepath
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return None

if __name__ == "__main__":
    # URL from the prompt
    url = "https://data.scryfall.io/all-cards/all-cards-20250403092149.json"
    
    # Allow specifying a custom URL via command line
    if len(sys.argv) > 1:
        url = sys.argv[1]
    
    download_scryfall_data(url)
