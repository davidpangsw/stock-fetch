from config import DIR_DATA
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import os

# https://finviz.com/screener.ashx?v=411&f=cap_midover,geo_usa&r=1000
# https://finviz.com/screener.ashx?v=411&f=cap_largeover%2Cgeo_usa&o=-marketcap
# v=411 (View Tickers only)
# f (filter)
#   cap_largeover (Large cap or above)
#   geo_usa (USA stocks)
# r (pagination)
#   1000 (page 1)
#   1001 (page 2)
# o (order)
#   -marketcap (By marketcap desc)
# ...
def scrape_symbols():
    url = "https://finviz.com/screener.ashx?v=411&f=cap_largeover%2Cgeo_usa&o=-marketcap"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Step 1: Download the HTML content to a local file
    raw_html_path = f'{DIR_DATA}/symbols/raw_page.html'
    os.makedirs(os.path.dirname(raw_html_path), exist_ok=True)  # Ensure directory exists
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    
    with open(raw_html_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    print(f"Saved raw HTML to {raw_html_path}")
    
    # Step 2: Read the local HTML file and parse tickers
    with open(raw_html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    print("Looking for screener_tickers")
    td = soup.find('td', class_='screener_tickers')
    if td is None:
        raise ValueError("Could not find td with class 'screener_tickers'")
    
    spans = td.find_all('span')
    symbols = [span.get_text().strip() for span in spans if span.get_text().strip()]
    
    symbols_path = f'{DIR_DATA}/symbols/symbols_raw.txt'
    os.makedirs(os.path.dirname(symbols_path), exist_ok=True)  # Ensure directory exists
    with open(symbols_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(symbols))
    
    print(f"Extracted {len(symbols)} symbols and saved to {symbols_path}")
    
    return symbols

def get_symbols(n=None):
    with open(f'{DIR_DATA}/symbols/symbols.txt') as file:
        lines = [line.rstrip() for line in file]
    with open(f'{DIR_DATA}/symbols/blacklist.txt') as file:
        blacklist = [line.rstrip() for line in file]
    
    lines = filter(lambda i: i not in blacklist, lines)
    lines = lines if n is None else list(lines)[0:n]
    return lines
