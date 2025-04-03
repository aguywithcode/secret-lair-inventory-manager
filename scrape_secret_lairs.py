#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
import re
import os

def scrape_secret_lairs():
    print("Scraping Secret Lair data...")
    url = "https://mtg.wiki/page/Secret_Lair/Drop_Series"
    
    # Send HTTP request to the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page: Status code {response.status_code}")
        return None
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table containing Secret Lair data
    # The table likely has class 'wikitable' or similar
    tables = soup.find_all('table', class_='wikitable')
    if not tables:
        print("Could not find any tables on the page")
        return None
    
    # Assuming the main Secret Lair table is the first matching table
    main_table = tables[0]
    
    # Initialize list to store all Secret Lair drops
    secret_lairs = []
    
    # Process table rows (skip header row)
    for row in main_table.find_all('tr')[1:]:
        columns = row.find_all('td')
        if len(columns) >= 3:  # Ensure we have at least the columns we need
            # Extract drop number
            drop_number = columns[0].text.strip()
            
            # Extract name
            name = columns[1].text.strip()
            
            # Extract card numbers
            card_numbers = columns[2].text.strip()
            
            # Create a dictionary for this Secret Lair drop
            secret_lair = {
                "drop_number": drop_number,
                "name": name,
                "card_numbers": card_numbers
            }
            
            # Add to our list
            secret_lairs.append(secret_lair)
    
    print(f"Found {len(secret_lairs)} Secret Lair drops")
    return secret_lairs

def save_to_json(data, filename="secret_lairs.json", directory="data"):
    """Save the scraped data to a JSON file in the data directory"""
    # Create the data directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Save the file to the data directory
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Data saved to {filepath}")

if __name__ == "__main__":
    secret_lairs = scrape_secret_lairs()
    if secret_lairs:
        save_to_json(secret_lairs)
    else:
        print("Failed to scrape Secret Lair data")
