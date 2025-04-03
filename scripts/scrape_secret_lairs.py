#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
import re
import os

def load_scryfall_data(filepath="data/scryfall_data.json"):
    """Load the Scryfall card data from the JSON file"""
    print(f"Loading Scryfall data from {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"Loaded {len(data)} cards from Scryfall data")
            return data
    except FileNotFoundError:
        print(f"Error: Scryfall data file not found at {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in Scryfall data file")
        return None

def parse_card_number_range(card_numbers_str):
    """Parse the card number range from a string like 'SLD-123 - SLD-129' or mixed formats"""
    # Common formats:
    # "SLD-123 - SLD-129" (range with set code)
    # "012 - 016" (simple number range without set code)
    # "SLD-123, SLD-125, SLD-127" (list)
    # "SLD-123" (single card)
    # "SLD-123 - SLD-129, SLD-135, SLD-140" (mixed format)
    
    # Clean up the string
    card_numbers_str = card_numbers_str.strip()
    
    # Initialize variables to store all collector numbers and the set code
    all_numbers = []
    set_code = None
    default_set_code = "SLD"  # Default set code if none is found
    
    # Process each part (split by commas)
    parts = [part.strip() for part in card_numbers_str.split(',')]
    
    for part in parts:
        # Check if this part is a range with hyphen in the format "SET-NUM - SET-NUM"
        range_match = re.search(r'([A-Z0-9]+)-(\d+)\s*-\s*([A-Z0-9]+)-(\d+)', part)
        if range_match:
            start_set = range_match.group(1)
            start_num = int(range_match.group(2))
            end_set = range_match.group(3)
            end_num = int(range_match.group(4))
            
            # Set the set_code if this is the first valid entry
            if set_code is None:
                set_code = start_set
            # Ensure sets match
            elif set_code != start_set or start_set != end_set:
                print(f"Warning: Set code mismatch in {part}")
                continue
                
            # Add all numbers in the range to our list
            all_numbers.extend(range(start_num, end_num + 1))
            continue
            
        # Check for simple number range format like "012 - 016"
        simple_range_match = re.search(r'(\d+)\s*-\s*(\d+)', part)
        if simple_range_match:
            start_num = int(simple_range_match.group(1))
            end_num = int(simple_range_match.group(2))
            
            # If we don't have a set code yet, use the default (SLD)
            if set_code is None:
                set_code = default_set_code
                print(f"Using default set code '{set_code}' for range {part}")
                
            # Add all numbers in the range to our list
            all_numbers.extend(range(start_num, end_num + 1))
            continue
        
        # Check for a single card entry
        single_match = re.search(r'([A-Z0-9]+)-(\d+)', part)
        if single_match:
            current_set = single_match.group(1)
            num = int(single_match.group(2))
            
            # Set the set_code if this is the first valid entry
            if set_code is None:
                set_code = current_set
            # Ensure sets match
            elif set_code != current_set:
                print(f"Warning: Set code mismatch in {part}")
                continue
                
            # Add this number to our list
            all_numbers.append(num)
            continue
            
        # Check for a simple number format (without set code)
        simple_num_match = re.search(r'^(\d+)$', part)
        if simple_num_match:
            num = int(simple_num_match.group(1))
            
            # If we don't have a set code yet, use the default (SLD)
            if set_code is None:
                set_code = default_set_code
                print(f"Using default set code '{set_code}' for number {num}")
                
            # Add this number to our list
            all_numbers.append(num)
            continue
    
    # If we found any valid numbers and a set code
    if all_numbers and set_code:
        # Sort and remove duplicates
        all_numbers = sorted(list(set(all_numbers)))
        print(f"Identified set {set_code} with collector numbers: {all_numbers}")
        return {
            'type': 'list',
            'set': set_code,
            'numbers': all_numbers
        }
    
    print(f"Warning: Could not parse card number format: {card_numbers_str}")
    return None

def find_matching_cards(scryfall_data, card_range):
    """Find cards in Scryfall data that match the given card number range"""
    if not card_range or not scryfall_data:
        return []
    
    matching_cards = []
    set_code = card_range['set']
    
    # SLD set code in Scryfall is lowercase
    scryfall_set_code = set_code.lower()
    
    print(f"Looking for cards in set '{scryfall_set_code}' with numbers: {card_range['numbers'] if 'numbers' in card_range else '?'}")
    
    # Filter to just SLD cards first for efficiency
    sld_cards = [card for card in scryfall_data if card.get('set', '') == scryfall_set_code]
    print(f"Found {len(sld_cards)} cards with set code '{scryfall_set_code}'")
    
    for card in sld_cards:
        collector_number = card.get('collector_number', '')
        
        # Some collector numbers might have non-numeric characters, like "123a"
        # Extract the numeric part for comparison
        collector_num_match = re.search(r'(\d+)', collector_number)
        if not collector_num_match:
            continue
        
        card_num = int(collector_num_match.group(1))
        
        # Check if this card's number is in our list
        if card_range['type'] == 'list' and card_num in card_range['numbers']:
            print(f"Matched: {card.get('name')} #{collector_number}")
            matching_cards.append(card)
    
    print(f"Found {len(matching_cards)} matching cards from set {set_code}")
    return matching_cards

def scrape_secret_lairs(match_with_scryfall=False, scryfall_filepath="data/scryfall_data.json"):
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
    tables = soup.find_all('table', class_='wikitable')
    if not tables:
        print("Could not find any tables on the page")
        return None
    
    # Assuming the main Secret Lair table is the first matching table
    main_table = tables[0]
    
    # Load Scryfall data if we want to match cards
    scryfall_data = None
    if match_with_scryfall:
        scryfall_data = load_scryfall_data(scryfall_filepath)
        if not scryfall_data:
            print("Warning: Could not load Scryfall data. Proceeding without card matching.")
            match_with_scryfall = False
    
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
            
            # If matching with Scryfall, find and add the matching cards
            if match_with_scryfall and scryfall_data:
                card_range = parse_card_number_range(card_numbers)
                if card_range:
                    matching_cards = find_matching_cards(scryfall_data, card_range)
                    
                    # Add basic card info to our Secret Lair object
                    card_list = []
                    for card in matching_cards:
                        # Get price data from the card object
                        prices = card.get("prices", {})
                        
                        card_list.append({
                            "name": card.get("name", "Unknown"),
                            "collector_number": card.get("collector_number", ""),
                            "set": card.get("set", ""),
                            "id": card.get("id", ""),
                            "image_uri": card.get("image_uris", {}).get("normal", ""),
                            "prices": {
                                "usd": prices.get("usd"),
                                "usd_foil": prices.get("usd_foil"),
                                "eur": prices.get("eur"),
                                "eur_foil": prices.get("eur_foil"),
                                "tix": prices.get("tix")
                            }
                        })
                    
                    secret_lair["cards"] = card_list
            
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
    # When run directly, match with Scryfall data
    secret_lairs = scrape_secret_lairs(match_with_scryfall=True)
    if secret_lairs:
        save_to_json(secret_lairs)
    else:
        print("Failed to scrape Secret Lair data")