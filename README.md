# Forex Historical Data Downloader

A Python tool to automatically download historical forex (FX) data from HistData.com. This tool supports downloading 1-minute timeframe data for multiple currency pairs.

## Features

- Automated download of forex historical data
- Supports multiple currency pairs (configurable in `config.py`)
- Downloads 1-minute timeframe data
- Automatic extraction of downloaded ZIP files
- Retry mechanism for failed downloads
- Detailed download progress and error reporting
- Failed downloads tracking for later retry
- Also repeats 

## Requirements

- Python 3.6+
- Chrome browser (for Selenium WebDriver)
- Required Python packages (install using requirements.txt)

## Installation

1. Clone this repository
2. Install required packages:

```powershell
pip install -r requirements.txt
```

## Configuration

Edit `config.py` to set:
- Currency pairs (PAIRS)
- Year (YEAR)
- Timeframe (default is M1 - 1 minute)

Default currency pairs:
- EURUSD
- GBPJPY
- USDJPY
- AUDUSD
- GBPUSD

## Usage

Run the script using:

```powershell
python main.py
```

The script will:
1. Create necessary directories (data/ and downloads/)
2. Download data for each configured currency pair
3. Extract downloaded files to pair-specific folders
4. Track and report any failed downloads

## Directory Structure

- `data/` - Extracted data files organized by currency pair
- `downloads/` - Downloaded ZIP files
- `config.py` - Configuration settings
- `downloader.py` - Download functionality
- `extractor.py` - ZIP extraction functionality
- `main.py` - Main script
- `failed_downloads.txt` - List of failed downloads (created if needed)

## Error Handling

- The script will retry failed downloads up to 3 times
- Failed downloads are logged to `failed_downloads.txt`
- Detailed error messages are displayed during execution

## Notes

- Downloads are performed using Selenium WebDriver
- The tool navigates HistData.com automatically
- Downloads may take some time depending on file sizes and internet connection
- Some IP addresses might be rate-limited by HistData.com
