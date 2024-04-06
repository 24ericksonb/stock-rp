import argparse
import datetime
import pygame
import requests
import time
from bs4 import BeautifulSoup

X = 480
Y = 320
LARGE_FONT = 45
SMALL_FONT = 20

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
    parser.add_argument('--refresh', type=check_positive, default=30, help='Refresh rate in seconds (default: 30, min: 1)')
    args = parser.parse_args()
    return args


def format_date(dt):
    """Format the given datetime object to a human-readable string."""
    day_suffix = ['th', 'st', 'nd', 'rd'] + ['th'] * 16 + ['st', 'nd', 'rd'] + ['th'] * 7 + ['st']
    formatted_date = dt.strftime(f'%A, %B %-d{day_suffix[dt.day - 1]} %-I:%M %p')
    return formatted_date


def get_stock_data(ticker):
    """Fetch stock data from CNBC for the given ticker."""
    url = f'https://www.cnbc.com/quotes/{ticker}'

    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        return -1.0, -1.0, -1.0
    
    if response.status_code != 200:
        return -1.0, -1.0, -1.0
    
    soup = BeautifulSoup(response.text, 'html.parser')
    element = soup.find('div', {'class': 'QuoteStrip-lastPriceStripContainer'})
    spans = element.find_all('span')

    last_price = float(spans[0].text.replace(',', ''))

    if spans[2].text == 'UNCH':
        price_change = 0.0
        percent_change = 0.0
    else:
        price_change = float(spans[1].text.split(' ')[0].strip('+'))
        percent_change = float(spans[1].text.split(' ')[1].strip('()+%'))

    return last_price, price_change, percent_change


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
    stock_text = font.render(f'{stock_name}    {price:,.2f}', True, color)
    change_text = font.render(f'{plus_sign}{change:,.2f}   {plus_sign}{percent_change:,.2f}%', True, color)
    stock_rect = stock_text.get_rect(center=(X // 2, position))
    change_rect = change_text.get_rect(center=(X // 2, position + LARGE_FONT + 5))
    display_surface.blit(stock_text, stock_rect)
    display_surface.blit(change_text, change_rect)


def main():
    """Main function for the stock ticker display."""
    args = parse_arguments()
    tickers = args.ticker
    refresh_rate = args.refresh

    pygame.init()

    pygame.mouse.set_visible(False)
    display_surface = pygame.display.set_mode((X, Y), pygame.NOFRAME)
    font = pygame.font.Font('font.ttf', LARGE_FONT)
    small_font = pygame.font.Font('font.ttf', SMALL_FONT)
    last_update_time = time.time() - refresh_rate
    update_interval = refresh_rate
    clock = pygame.time.Clock()
    background = pygame.image.load('background.png')

    while True:
        current_time = time.time()
        if current_time - last_update_time >= update_interval:
            display_surface.blit(background, (0, 0))
            last_updated = format_date(datetime.datetime.now())
            for i, ticker in enumerate(tickers):
                price, change, percent_change = get_stock_data(ticker)
                render_stock_info(display_surface, font, ticker, price, change, percent_change,
                                   (LARGE_FONT * 1.25) + i * (LARGE_FONT * 2.75))
            render_last_updated(display_surface, small_font, last_updated)
            last_update_time = current_time

            # Flip the display surface upside down and blit it onto the screen
            flipped_surface = pygame.transform.rotate(display_surface, 180)
            display_surface.blit(flipped_surface, (0, 0))

        # Update the entire display
        pygame.display.flip()
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

if __name__ == '__main__':
    main()


if __name__ == '__main__':
    main()
