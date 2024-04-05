import argparse
import datetime
import pygame
import requests
import time
from bs4 import BeautifulSoup

# Constants for display dimensions and font sizes
X = 480
Y = 320
LARGE_FONT = 45
SMALL_FONT = 20


def parse_arguments():
    """Parse command line arguments for stock tickers."""
    parser = argparse.ArgumentParser(description='Stock Ticker Display')
    parser.add_argument('ticker', nargs=2, help='Two stock tickers')
    args = parser.parse_args()
    return args


def get_stock_data(ticker):
    """Fetch stock data from CNBC for the given ticker."""
    url = f'https://www.cnbc.com/quotes/{ticker}'
    response = requests.get(url)
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
    updated_text = font.render(f'Last Updated: {last_updated}', True, white)
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
    change_text = font.render(f'{plus_sign}{change:,.2f}, {plus_sign}{percent_change:,.2f}%', True, color)
    stock_rect = stock_text.get_rect(center=(X // 2, position))
    change_rect = change_text.get_rect(center=(X // 2, position + LARGE_FONT + 5))
    display_surface.blit(stock_text, stock_rect)
    display_surface.blit(change_text, change_rect)


def main():
    """Main function for the stock ticker display."""
    args = parse_arguments()
    tickers = args.ticker

    pygame.init()

    display_surface = pygame.display.set_mode((X, Y), pygame.NOFRAME)
    font = pygame.font.Font('font.ttf', LARGE_FONT)
    small_font = pygame.font.Font('font.ttf', SMALL_FONT)
    last_update_time = time.time() - 5
    update_interval = 5
    clock = pygame.time.Clock()
    background = pygame.image.load('background.png')

    while True:
        current_time = time.time()
        if current_time - last_update_time >= update_interval:
            display_surface.blit(background, (0, 0))
            last_updated = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for i, ticker in enumerate(tickers):
                price, change, percent_change = get_stock_data(ticker)
                render_stock_info(display_surface, font, ticker, price, change, percent_change,
                                   (LARGE_FONT * 1.25) + i * (LARGE_FONT * 2.75))
            render_last_updated(display_surface, small_font, last_updated)
            last_update_time = current_time
        pygame.display.update()
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


if __name__ == '__main__':
    main()
