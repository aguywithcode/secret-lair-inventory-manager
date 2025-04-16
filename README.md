# MTG Inventory Manager

A tool for Magic: The Gathering collectors to track Secret Lair products and card values.

## Overview

The **MTG Inventory Manager** helps collectors track their Magic: The Gathering inventory, with a focus on Secret Lair products. It fetches the latest card data from Scryfall and scrapes Secret Lair information from the MTG Wiki to create a comprehensive database of cards and their current market values.

## Features

- **Data Collection**:
  - Automatic download of the latest card data from Scryfall
  - Scraping of Secret Lair drop information from MTG Wiki
  - Matching Secret Lair products with corresponding cards in Scryfall

- **Price Tracking**:
  - Regular and foil price information for all cards
  - Calculation of total value for Secret Lair drops

- **Web Interface**:
  - Browse all Secret Lair drops
  - View detailed information about each drop, including cards and prices
  - Search functionality to find specific Secret Lairs
  - Responsive design that works on desktop and mobile devices

- **Developer Features**:
  - REST API endpoints for programmatic access to data
  - Configurable logging with different verbosity levels
  - Command-line tools with helpful arguments

## Installation

### Requirements

- Python 3.8+
- pip (Python package manager)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/aguywithcode/secret-lair-inventory-manager.git
   cd mtg_inventory_manager
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize data:
   ```bash
   python init_data.py
   ```
   This will download the latest Scryfall data and scrape Secret Lair information.

## Usage

### Data Management

Initialize or update data:
```bash
python init_data.py [--force] [--verbose]
```
Options:
- `--force` or `-f`: Force download of Scryfall data even if recent data exists
- `--verbose` or `-v`: Enable detailed debug output

### Web Interface

Run the web interface:
```bash
python run_web.py [--host HOST] [--port PORT] [--debug]
```

Options:
- `--host`: Host to bind to (default: 127.0.0.1)
- `--port`: Port to bind to (default: 5000)
- `--debug`: Run in debug mode

Then open your browser and navigate to `http://localhost:5000/` (or the host/port you specified).

### Individual Scripts

You can also run the individual scripts directly:

- Download Scryfall data:
  ```bash
  python scripts/download_scryfall_data.py [--force] [--verbose]
  ```

- Scrape Secret Lair data:
  ```bash
  python scripts/scrape_secret_lairs.py [--verbose]
  ```

## Project Structure

```
mtg_inventory_manager/
├── data/                     # Directory for storing fetched and processed data
├── scripts/                  # Python scripts for data processing
│   ├── download_scryfall_data.py
│   ├── scrape_secret_lairs.py
│   ├── initialize_data.py
├── web/                      # Web interface files
│   ├── app.py                # Flask application
│   ├── templates/            # HTML templates
│   ├── static/               # Static files (CSS, JS)
├── .gitignore                # Git ignore file
├── init_data.py              # Launcher script for data initialization
├── run_web.py                # Launcher script for the web interface
├── requirements.txt          # Python dependencies
├── history.md                # Development history
└── README.md                 # This file
```

## API Endpoints

The web interface provides the following REST API endpoints:

- `GET /api/secret-lairs`: Returns a list of all Secret Lair drops
- `GET /api/secret-lair/<drop_number>`: Returns details about a specific Secret Lair drop

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Scryfall](https://scryfall.com/) for providing card data
- [MTG Wiki](https://mtg.wiki/) for Secret Lair information
