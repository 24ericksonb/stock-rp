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

To add a minimum value constraint for the `refresh` argument in the `parse_arguments` function, you can use the `choices` parameter of `add_argument` to specify a range of acceptable values. Here's how you can modify the function:

```python
def parse_arguments():
    """Parse command line arguments for stock tickers."""
    parser = argparse.ArgumentParser(description='Stock Ticker Display')
    parser.add_argument('ticker', nargs=2, help='Two stock tickers')
    parser.add_argument('--refresh', type=int, default=5, help='Refresh rate in seconds (default: 5, min: 1)')
    args = parser.parse_args()
    return args
```

## Usage
- Run the script with the following command:
  ```
  python3 stock_ticker.py <ticker-1> <ticker-2>
  ```
- You can also specify the refresh rate in seconds using the `--refresh` option (minimum 1 second, default 10 seconds):
  ```
  python3 stock_ticker.py <ticker-1> <ticker-2> --refresh <speed-in-seconds>
  ```
- Example command:
  ```
  python3 stock_ticker.py RBLX SPX --refresh 10
  ```
- The stock ticker display will show the current prices and changes for the specified stocks, updating at the specified refresh rate (WARNING: becareful of rate limit if set to a low speed).
- To exit the program, press `CTRL+C` in the terminal or close the terminal window.

## Customization
- You can modify the stock tickers by changing the arguments when running the script.
- The update interval and display settings can be adjusted in the `stock_ticker.py` file.

## License
This project is open-source and available under the MIT License.

---
