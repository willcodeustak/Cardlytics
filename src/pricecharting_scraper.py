from bs4 import BeautifulSoup
import pandas as pd
import requests
from config import PRICECHARTING

def fetch_pricecharting_data(search_term):
    url = f"https://www.pricecharting.com/search-products?q={search_term.replace(' ', '+')}&type=prices"
    try:
        response = requests.get(url, 
                             headers=PRICECHARTING['HEADERS'],
                             timeout=10)
        response.raise_for_status()
        
        with open('debug.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        return response.text
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return None

def parse_pricecharting_html(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        table = (soup.find('table', {'class': 'table-prices'}) or 
                soup.find('table', {'id': 'games_table'}))
        
        if not table:
            print("Debug: No price table found in HTML")
            return pd.DataFrame()
            
        listings = []
        for row in table.find_all('tr')[1:]:  # Skip header row
            cols = row.find_all('td')
            if len(cols) >= 5:
                price_text = cols[3].get_text(strip=True).replace('$', '')
                listings.append({
                    'name': cols[0].get_text(strip=True),
                    'condition': cols[1].get_text(strip=True),
                    'price': float(price_text) if price_text.replace('.', '').isdigit() else None
                })
                
        return pd.DataFrame(listings)
        
    except Exception as e:
        print(f"Error parsing HTML: {str(e)}")
        return pd.DataFrame()