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

### Development with VS Code Devcontainer

This project includes a devcontainer configuration for seamless development in Visual Studio Code.

#### Prerequisites
- [VS Code](https://code.visualstudio.com/) installed
- [Docker](https://www.docker.com/products/docker-desktop) installed and running
- [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension installed in VS Code

#### Setup with Devcontainer
1. Open the project folder in VS Code
2. When prompted, click "Reopen in Container", or run the "Remote-Containers: Reopen in Container" command from the command palette
3. VS Code will build the container and set up the development environment automatically
4. Once the container is ready, all dependencies will be installed and the environment will be fully configured

#### Features
The devcontainer comes with:
- Python 3.12 with pip pre-installed
- Git pre-installed and configured 
- Node.js and npm pre-installed for JavaScript development
- VS Code extensions for Python and JavaScript development
- Port forwarding for the web application (port 5000)
- Automatic dependency installation from requirements.txt

#### Running the Application
Once in the devcontainer, you can initialize data and run the web server using the same commands:
```bash
python init_data.py
python run_web.py
```

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

## Docker Deployment

The application can be easily deployed using Docker:

### Using Docker Compose (Recommended)

1. Build and start the container:
   ```bash
   docker-compose up -d
   ```

2. Access the web interface at `http://localhost:5000`

3. Stop the container:
   ```bash
   docker-compose down
   ```

### Using Docker Directly

1. Build the Docker image:
   ```bash
   docker build -t mtg-inventory-manager .
   ```

2. Run the container:
   ```bash
   docker run -d -p 5000:5000 -v "$(pwd)/data:/app/data" --name mtg-inventory-manager mtg-inventory-manager
   ```

3. Access the web interface at `http://localhost:5000`

4. Stop the container:
   ```bash
   docker stop mtg-inventory-manager
   docker rm mtg-inventory-manager
   ```

### Docker Configuration

- The container automatically downloads Scryfall data and scrapes Secret Lair information on startup
- Data is persisted in a volume mapped to the local `./data` directory
- The web interface is available on port 5000
- The container includes all dependencies:
  - Python 3.12 with required packages
  - Git for version control
  - Node.js and ESLint for JavaScript support

## Testing

The project includes a comprehensive test suite using pytest:

### Setting Up the Test Environment

1. Install test dependencies:
   ```bash
   pip install -r tests/requirements-test.txt
   ```

2. Run all tests:
   ```bash
   pytest
   ```

3. Run tests with coverage report:
   ```bash
   pytest --cov
   ```

4. Generate a detailed HTML coverage report:
   ```bash
   pytest --cov --cov-report=html
   ```
   This will create a `htmlcov` directory with an interactive coverage report you can view in your browser.

### Test Organization

- `tests/test_download_scryfall_data.py`: Tests for the Scryfall data downloader
- `tests/test_scrape_secret_lairs.py`: Tests for the Secret Lair data scraper
- `tests/test_initialize_data.py`: Tests for the data initialization process
- `tests/test_web_app.py`: Tests for the Flask web application

## Project Structure

```
mtg_inventory_manager/
├── data/                     # Directory for storing fetched and processed data
├── scripts/                  # Python scripts for data processing
│   ├── download_scryfall_data.py
│   ├── scrape_secret_lairs.py
│   ├── initialize_data.py
├── tests/                    # Unit and integration tests
│   ├── __init__.py
│   ├── requirements-test.txt
│   ├── test_*.py             # Test files
├── web/                      # Web interface files
│   ├── app.py                # Flask application
│   ├── templates/            # HTML templates
│   ├── static/               # Static files (CSS, JS)
├── .gitignore                # Git ignore file
├── init_data.py              # Launcher script for data initialization
├── pytest.ini                # Pytest configuration
├── requirements.txt          # Python dependencies
├── run_web.py                # Launcher script for the web interface
├── LICENSE                   # License information
└── README.md                 # This file
```

## API Endpoints

The web interface provides the following REST API endpoints:

- `GET /api/secret-lairs`: Returns a list of all Secret Lair drops
- `GET /api/secret-lair/<drop_number>`: Returns details about a specific Secret Lair drop

## Contributing

We welcome contributions to the MTG Inventory Manager project! Here's how you can help:

### Setting Up Development Environment

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/mtg_inventory_manager.git`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up the data: `python init_data.py`
5. Run the development server: `python run_web.py --debug`

### Contribution Guidelines

1. **Create an Issue**: For new features or bugs, start by creating an issue to discuss it
2. **Branch Naming**: Use descriptive branch names (`feature/collection-tracking`, `bugfix/price-display`)
3. **Code Style**: Follow PEP 8 style guidelines for Python code
4. **Documentation**: Update documentation for any changes to functionality
5. **Testing**: Add tests for new features and ensure existing tests pass
6. **Commit Messages**: Write clear commit messages that explain the changes

### Pull Request Process

1. Update the README.md or other documentation if needed
2. Update the history.md file with a description of your changes
3. Submit the Pull Request with a clear description of the changes
4. Address any feedback from the code review

### Getting Help

If you need help with contributing, feel free to:
- Open an issue with questions
- Ask for clarification on existing issues
- Reach out to the maintainers

## Future Development

See our [Development Roadmap](roadmap.md) for planned features and improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Scryfall](https://scryfall.com/) for providing card data
- [MTG Wiki](https://mtg.wiki/) for Secret Lair information
