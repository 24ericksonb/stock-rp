import argparse
import datetime
import pygame
import time
import socket
import yfinance as yf

X = 480
Y = 320
LARGE_FONT = 45
SMALL_FONT = 20
TINY_FONT = 12
RETRIES = 10

def get_ip_address():
    """Get the IP address of the device."""
    for _ in range(RETRIES):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
        except Exception:
            print("Failed to find IP address. Retrying...")
            time.sleep(4)
            continue
        return ip_address
    print("No IP address found. Exiting...")
    exit()


def check_positive(value):
    """Check if the given value is a positive integer."""
    ivalue = int(value)
    if ivalue < 1:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    return ivalue

def parse_arguments():
    """Parse command line arguments for stock tickers."""
    parser = argparse.ArgumentParser(description='Stock Ticker Display')
    parser.add_argument('ticker', nargs=2, help='Two stock tickers')
    parser.add_argument('--refresh', type=check_positive, default=1, help='Refresh rate in seconds (default: 1, min: 1)')
    args = parser.parse_args()
    return args


def format_date(dt):
    """Format the given datetime object to a human-readable string."""
    day_suffix = ['th', 'st', 'nd', 'rd'] + ['th'] * 16 + ['st', 'nd', 'rd'] + ['th'] * 7 + ['st']
    formatted_date = dt.strftime(f'%A, %B %-d{day_suffix[dt.day - 1]} %-I:%M %p')
    return formatted_date


def get_stock_data(ticker):
    try:
        data = yf.Ticker(ticker).info
        price = data.get('currentPrice')
        previous_close = data['regularMarketPreviousClose']
        change = price - previous_close
        percent_change = (change / previous_close) * 100
        return float(price), float(change), float(percent_change)
    except Exception:
        return -1.0, -1.0, -1.0


def render_last_updated(display_surface, font, last_updated):
    """Render the last updated time on the display surface."""
    white = (255, 255, 255)
    updated_text = font.render(f'Updated: {last_updated}', True, white)
    updated_rect = updated_text.get_rect(center=(X // 2, Y - SMALL_FONT))
    display_surface.blit(updated_text, updated_rect)


def render_stock_info(display_surface, font, stock_name, price, change, percent_change, position):
    """Render stock information on the display surface."""
    white = (255, 255, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)
    color = green if change > 0 else red if change < 0 else white
    plus_sign = '+' if change > 0 else ''

    errored = price == -1
    price_text = 'ERROR' if errored else f'${price:,.2f}'
    change_text = 'ERROR' if errored else f'{plus_sign}${change:,.2f}'
    percent_change_text = 'ERROR' if errored else f'{plus_sign}{percent_change:,.2f}%'

    stock_text = font.render(f'{stock_name}    {price_text}', True, color)
    change_text = font.render(f'{change_text}   {percent_change_text}', True, color)
    stock_rect = stock_text.get_rect(center=(X // 2, position))
    change_rect = change_text.get_rect(center=(X // 2, position + LARGE_FONT + 5))

    display_surface.blit(stock_text, stock_rect)
    display_surface.blit(change_text, change_rect)


def render_ip_address(display_surface, font, ip_address):
    """Render the IP address on the display surface."""
    white = (255, 255, 255)
    ip_text = font.render(f'IP: {ip_address}', True, white)
    display_surface.blit(ip_text, (10, 10))


def main():
    """Main function for the stock ticker display."""
    ip_address = get_ip_address()
        
    args = parse_arguments()
    tickers = args.ticker
    refresh_rate = args.refresh - 1

    pygame.init()

    pygame.mouse.set_visible(False)
    display_surface = pygame.display.set_mode((X, Y), pygame.NOFRAME)
    font = pygame.font.Font('font.ttf', LARGE_FONT)
    small_font = pygame.font.Font('font.ttf', SMALL_FONT)
    tiny_fony = pygame.font.Font('font.ttf', TINY_FONT)
    last_update_time = time.time() - refresh_rate
    update_interval = refresh_rate
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        current_time = time.time()

        if current_time - last_update_time >= update_interval:
            display_surface.fill((0, 0, 0)) 
            last_updated = format_date(datetime.datetime.now())
            for i, ticker in enumerate(tickers):
                price, change, percent_change = get_stock_data(ticker) 
                render_stock_info(display_surface, font, ticker, price, change, percent_change,
                                   (LARGE_FONT * 1.5) + i * (LARGE_FONT * 2.75))
            render_last_updated(display_surface, small_font, last_updated)
            render_ip_address(display_surface, tiny_fony, ip_address)
            last_update_time = current_time

            flipped_surface = pygame.transform.rotate(display_surface, 180)
            display_surface.blit(flipped_surface, (0, 0))

        pygame.display.flip()
        clock.tick(1.0 / (refresh_rate + 1))

if __name__ == '__main__':
    main()
