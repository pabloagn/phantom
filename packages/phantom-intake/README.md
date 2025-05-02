# Phantom Intake

A sleek utility for downloading files from LibGen via IPFS links with proper error handling, advanced logging, and beautiful terminal progress indication.

## Features

- Clean, modular code structure following industry standards
- Comprehensive type hints for better code maintainability
- Rich terminal UI with colorful progress bars
- Configurable LibGen domains and IPFS gateways
- Smart retry mechanism with exponential backoff
- Detailed logging with standard formats
- YAML configuration system for easy customization
- Error tracking and detailed reporting

## Installation

### From Source

1. Clone this repository:
```bash
git clone https://github.com/Phantomklange/phantom-intake.git
cd phantom-intake
```

2. Install the package in development mode:
```bash
pip install -e .
```

### Using pip (if published to PyPI)

```bash
pip install phantom-intake
```

## Usage

### Basic Usage

1. Create the input directory and place your download URLs in a file named `download.txt`:
```bash
mkdir -p input
echo "https://libgen.url/example" > input/download.txt
```

2. Run the script:
```bash
python phantom-intake.py
```

### Configuration

The application uses a YAML configuration file (`config.yaml`) that is created automatically on first run. You can modify this file to customize the application's behavior:

```yaml
# Directory paths
input_dir: input
output_dir: outputs
log_dir: logs

# File settings
urls_file: download.txt

# Network settings
max_retries: 3
timeout_seconds: 30
delay_seconds: 2
user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"

# LibGen specific settings
libgen_domains:
  - libgen.is
  - libgen.li
  - libgen.rs

# IPFS settings
use_ipfs_gateway: true
ipfs_gateway_urls:
  - https://ipfs.io/ipfs/
  - https://dweb.link/ipfs/
```

### Configuration Options

- **input_dir**: Directory containing the URLs file
- **output_dir**: Directory where downloaded files will be saved
- **log_dir**: Directory for log files
- **urls_file**: Name of the file containing URLs to download
- **max_retries**: Maximum number of retry attempts for failed requests
- **timeout_seconds**: Timeout for HTTP requests
- **delay_seconds**: Delay between requests
- **user_agent**: User agent string to use for HTTP requests
- **libgen_domains**: List of LibGen domains to try if the URL doesn't specify a domain
- **use_ipfs_gateway**: Whether to use IPFS gateways
- **ipfs_gateway_urls**: List of IPFS gateway URLs to try

## Project Structure

```
phantom-intake/
├── phantom-intake.py    # Main entry point script
├── config.yaml          # Configuration file
├── phantom_intake/      # Package directory
│   ├── __init__.py      # Package initialization
│   ├── config.py        # Configuration handling
│   ├── downloader.py    # File downloading functionality
│   ├── scraper.py       # Web scraping functionality
│   └── utils.py         # Utility functions
├── input/               # Input directory for URL lists
│   └── download.txt     # File containing URLs to download
├── outputs/             # Directory for downloaded files
├── logs/                # Directory for log files
├── .gitignore           # Git ignore file
├── README.md            # Project documentation
├── requirements.txt     # Project dependencies
└── setup.py             # Setup script for installing the package
```

## Customizing for Your Environment

After installation, you can modify the configuration file to better suit your environment:

1. Adjust the paths in `config.yaml` if you want to store files in different locations
2. Update the LibGen domains if the current ones become unavailable
3. Add or modify IPFS gateways to improve download reliability

## License

This project is licensed under the MIT License - see the LICENSE file for details.