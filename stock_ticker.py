import argparse
import datetime
import pygame
import time
import socket
import subprocess
from yahooquery import Ticker

X = 480
Y = 320
LARGE_FONT = 42
SMALL_FONT = 15
TINY_FONT = 12
RETRIES = 10
AMOUNT_STOCK = 2627

def get_ip_address():
    """Get the IP address of the device."""
    for _ in range(RETRIES):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(2)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address
        except Exception:
            print("Failed to find IP address. Retrying...")
            time.sleep(4)
    print("No IP address found. Exiting...")
    exit()


def get_temperature():
    try:
        result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        temp_str = output.split('=')[1].split("'")[0]
        return float(temp_str)
    except Exception:
        return None


def check_positive(value):
    """Check if the given value is a positive integer."""
    ivalue = int(value)
    if ivalue < 1:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    return ivalue

def parse_arguments():
    """Parse command line arguments for stock tickers."""
    parser = argparse.ArgumentParser(description='Stock Ticker Display')
    parser.add_argument('ticker', help='Stock ticker')
    parser.add_argument('--refresh', type=check_positive, default=1, help='Refresh rate in seconds (default: 1, min: 1)')
    args = parser.parse_args()
    return args


def format_date(dt):
    """Format the given datetime object to a human-readable string."""
    day_suffix = ['th', 'st', 'nd', 'rd'] + ['th'] * 16 + ['st', 'nd', 'rd'] + ['th'] * 7 + ['st']
    day = dt.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    formatted_date = dt.strftime(f'%A, %B {day}{suffix} %I:%M %p')
    return formatted_date



def get_stock_data(ticker):
    try:
        ticker_obj = Ticker([ticker])
        return ticker_obj.price
    except Exception:
        return []


def parse_stock_data(data, ticker):
    price_data = {}

    try:
        ticker_data = data[ticker]
        price = ticker_data.get('regularMarketPrice')
        change = round(ticker_data.get('regularMarketChange'), 2)
        percent_change = round(ticker_data.get('regularMarketChangePercent') * 100, 2)
        price_data[ticker] = (float(price), float(change), float(percent_change))
    except Exception:
        price_data[ticker] = (-1.0, -1.0, -1.0)
    return price_data


def render_last_updated(display_surface, font, last_updated):
    """Render the last updated time on the display surface."""
    white = (255, 255, 255)
    updated_text = font.render(f'{last_updated}', True, white)
    updated_rect = updated_text.get_rect(center=(125, Y - SMALL_FONT))
    display_surface.blit(updated_text, updated_rect)


def render_text(display_surface, font, text, position):
    """Render any text on the display surface."""
    white = (255, 255, 255)

    main_text = font.render(text, True, white)
    main_text_rect = main_text.get_rect(center=(X // 2, position + LARGE_FONT // 2))

    display_surface.blit(main_text, main_text_rect)


def render_stock_info(display_surface, font, stock_name, price, change, percent_change, position):
    """Render stock information on the display surface."""
    white = (255, 255, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)
    color = green if change > 0 else red if change < 0 else white
    sign = '+' if change > 0 else '-' if change < 0 else ''

    errored = price == -1
    price_text = 'ERROR' if errored else f'${price:,.2f}'
    change_text = 'ERROR' if errored else f'{sign}${abs(change):,.2f}'
    percent_change_text = 'ERROR' if errored else f'{sign}{abs(percent_change):,.2f}%'

    stock_text = font.render(f'{stock_name}    {price_text}', True, color)
    change_text = font.render(f'{change_text}   {percent_change_text}', True, color)
    stock_rect = stock_text.get_rect(center=(X // 2, position))
    change_rect = change_text.get_rect(center=(X // 2, position + LARGE_FONT + 5))

    display_surface.blit(stock_text, stock_rect)
    display_surface.blit(change_text, change_rect)


def render_monitoring_data(display_surface, font, ip_address, temperature):
    """Render the IP address on the display surface."""
    white = (255, 255, 255)
    ip_address_text = f'IP: {ip_address}' if ip_address else 'N/A'
    temperature_text = f'{temperature}° C'
    ip_text = font.render(ip_address_text, True, white)
    temp_text = font.render(temperature_text, True, white)
    display_surface.blit(ip_text, (10, 10))
    if temperature:
        display_surface.blit(temp_text, (10, 10 + SMALL_FONT))


def render_market_status(display_surface, font, current_date):
    """Render the market status on the display surface."""
    market_status = 'Market Closed'
    position = (410, Y - SMALL_FONT)
    white = (255, 255, 255)
    current_hour_decimal = current_date.hour + current_date.minute / 60.0
    if current_date.weekday() < 5 and 9.5 <= current_hour_decimal < 16:
        market_status = 'Market Open'
        position = (417, Y - SMALL_FONT)
    market_text = font.render(f'{market_status}', True, white)
    market_rect = market_text.get_rect(center=position)
    display_surface.blit(market_text, market_rect)

def main():
    """Main function for the stock ticker display."""
    ip_address = get_ip_address()
        
    args = parse_arguments()
    ticker = args.ticker
    refresh_rate = args.refresh - 1

    pygame.init()

    pygame.mouse.set_visible(False)
    display_surface = pygame.display.set_mode((X, Y), pygame.NOFRAME)
    font = pygame.font.Font('font.ttf', LARGE_FONT)
    small_font = pygame.font.Font('font.ttf', SMALL_FONT)
    tiny_fony = pygame.font.Font('font.ttf', TINY_FONT)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display_surface.fill((0, 0, 0)) 
        current_date = datetime.datetime.now()
        last_updated = format_date(current_date)
        temperature = get_temperature()
        stock_data = get_stock_data(ticker)
        stock_info = parse_stock_data(stock_data, ticker)
        price, change, percent_change = stock_info[ticker]
        render_stock_info(display_surface, font, ticker, price, change, percent_change,
                            (LARGE_FONT * 2.25) + 0 * (LARGE_FONT * 3.25))
        total_stock = f"${price * AMOUNT_STOCK:,.2f}"
        render_text(display_surface, font, total_stock, (LARGE_FONT * 1.75) + 1 * (LARGE_FONT * 2.75))
        render_last_updated(display_surface, small_font, last_updated)
        render_monitoring_data(display_surface, tiny_fony, ip_address, temperature)
        render_market_status(display_surface, small_font, current_date)

        flipped_surface = pygame.transform.rotate(display_surface, 180)
        display_surface.blit(flipped_surface, (0, 0))
        pygame.display.flip()
        clock.tick(1.0 / (refresh_rate + 1))

if __name__ == '__main__':
    main()
