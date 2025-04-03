# MTG Inventory Manager - Development History

This document captures the development history of the MTG Inventory Manager project.

## Project Overview

The MTG Inventory Manager is a tool designed to help Magic: The Gathering collectors track their inventory, with particular focus on Secret Lair products. The system fetches data from Scryfall and scrapes information from the MTG Wiki to create a comprehensive database of cards.

## Development Timeline

### Initial Setup

1. Created a script to scrape Secret Lair drop information from MTG Wiki
   - Extracts drop number, name, and card numbers
   - Stores data in JSON format

2. Created a script to download bulk card data from Scryfall
   - Initially used hardcoded URL
   - Later updated to use Scryfall's Bulk Data API to always fetch the latest data
   - Added progress bar for large downloads
   - Implemented caching to avoid unnecessary downloads

3. Added essential project files:
   - `.gitignore` to exclude data files and Python artifacts
   - `requirements.txt` to manage dependencies

### Feature Development

4. Enhanced the Secret Lair scraper:
   - Added capability to match Secret Lair drops with card data from Scryfall
   - Implemented parsing for various card number formats:
     - Ranges with set codes (SLD-123 - SLD-129)
     - Simple number ranges (012 - 016)
     - Mixed formats with commas and ranges
     - Single card numbers
   - Added price information (foil and non-foil) from Scryfall data

5. Created data initialization script:
   - Combines functionality of download and scrape scripts
   - Shows clear progress information
   - Returns appropriate exit codes for automation

### Technical Improvements

6. Data directory organization:
   - All fetched and processed data stored in `/data` directory
   - Data directory excluded from git with `.gitignore`

7. Download optimization:
   - Check if Scryfall data has been updated within the last day
   - Skip downloads if data is recent to improve initialization speed
   - Added force flag option to override when needed

8. Parsing improvements:
   - Robust handling of various card number formats
   - Support for disjoint collector numbers (e.g., "1, 5, 9")
   - Default to SLD set code when not specified

9. Code organization:
   - Moved Python scripts to a dedicated `/scripts` directory
   - Created a simple launcher in the root directory
   - Improved project structure

10. Logging implementation:
    - Added proper Python logging framework to all scripts
    - Implemented --verbose flag to control output detail level
    - Intelligent progress bar display based on log level
    - Improved error handling with optional stack traces
    - More consistent user feedback across all operations

11. Logging refinements:
    - Reclassified card matching logs as debug level
    - Added summary statistics at info level
    - Better separation between normal and verbose output
    - Enhanced debugging information for card range processing

## Current Components

- `scripts/scrape_secret_lairs.py`: Scrapes Secret Lair drop data from MTG Wiki
- `scripts/download_scryfall_data.py`: Downloads latest card data from Scryfall API
- `scripts/initialize_data.py`: Combined script to set up all required data
- `init_data.py`: Simple launcher script in the root directory
- `requirements.txt`: Python package dependencies
- `.gitignore`: Configuration to exclude data and temporary files

## Future Development Ideas

- Create a UI for browsing Secret Lair drops
- Add collection tracking functionality
- Implement price trend analysis
- Support for other special products beyond Secret Lairs
