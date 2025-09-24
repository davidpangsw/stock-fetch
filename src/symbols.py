from config import DIR_DATA

# https://finviz.com/screener.ashx?v=411&f=cap_midover,geo_usa&r=1000
# v=411 (View Tickers only)
# f (filter)
#   cap_midover (Mid cap or above)
#   geo_usa (USA stocks)
# r (pagination)
#   1000 (page 1)
#   1001 (page 2)
# ...
def scrape_symbols():
    url = "https://finviz.com/screener.ashx?v=411&f=cap_midover,geo_usa&r=1000"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    soup = BeautifulSoup(response.content, 'html.parser')
    
    td = soup.find('td', class_='screen_tickers')
    if td is None:
        raise ValueError("Could not find td with class 'screen_tickers'")
    
    spans = td.find_all('span')
    symbols = [span.get_text().strip() for span in spans if span.get_text().strip()]
    
    with open('symbols_raw.txt', 'w') as f:
        f.write('\n'.join(symbols))
    
    print(f"Extracted {len(symbols)} symbols and saved to symbols_raw.txt")

    return symbols

def get_symbols(n=None):
    with open(f'{DIR_DATA}/symbols/symbols.txt') as file:
        lines = [line.rstrip() for line in file]
    with open(f'{DIR_DATA}/symbols/blacklist.txt') as file:
        blacklist = [line.rstrip() for line in file]
    
    lines = filter(lambda i: i not in blacklist, lines)
    lines = lines if n is None else list(lines)[0:n]
    return lines
