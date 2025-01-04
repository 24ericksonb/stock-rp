# Raspberry Pi Stock Ticker

## Overview
This project creates a stock ticker display for your desk using a Raspberry Pi and an LCD screen. It shows real-time stock prices and changes for two specified stocks, updating every few seconds.

## Requirements
- Raspberry Pi (any model with GPIO pins)
- LCD screen compatible with Raspberry Pi (480x320 resolution recommended)
- Internet connection for fetching stock data
- Python 3 with the following libraries (see requirements.txt):
  - `pygame`
  - `requests`
  - `beautifulsoup4`

## Setup

### Hardware Setup
1. Connect the LCD screen to your Raspberry Pi according to the manufacturer's instructions.
2. Ensure that your Raspberry Pi is connected to the internet.

### Software Setup
1. Clone this repository to your Raspberry Pi:
   ```
   git clone https://github.com/24ericksonb/stock-rp.git
   ```
2. Navigate to the project directory:
   ```
   cd stock-rp
   ```
3. Install the required Python libraries:
   ```
   pip3 install -r requirements.txt
   ```
4. Run the script with two stock tickers as arguments:
   ```
   python3 stock_ticker.py AAPL MSFT
   ```

## Usage
- Run the script with the following command:
  ```
  python3 stock_ticker.py <ticker>
  ```
- You can also specify the refresh rate in seconds using the `--refresh` option (minimum 1 second, default 10 seconds):
  ```
  python3 stock_ticker.py <ticker> --refresh <speed-in-seconds>
  ```
- Example command:
  ```
  python3 stock_ticker.py RBLX --refresh 10
  ```
- The stock ticker display will show the current prices and changes for the specified stocks, updating at the specified refresh rate (WARNING: becareful of rate limit if set to a low speed).
- To exit the program, press `CTRL+C` in the terminal or close the terminal window.
---
