from bs4 import BeautifulSoup
import re
import pandas as pd

def parse_ebay_html(html):
  try:
        soup = BeautifulSoup(html, 'lxml')
  except Exception as e:
        print(f"HTML parsing error: {str(e)}")
        return pd.DataFrame()
  listings = []
    
  items = soup.find_all('li', {'class': 's-item'})
    
  for item in items:
        price_tag = item.find('span', {'class': 's-item__price'})
        if not price_tag:
            continue
            
        price_text = re.sub(r'^[A-Za-z$ ]+', '', price_tag.get_text(strip=True))
        title_tag = item.find('h3', {'class': 's-item__title'})
        date_tag = item.find('span', {'class': 's-item__title--tagblock'})
        
        listings.append({
            'title': title_tag.get_text(strip=True) if title_tag else '',
            'price': price_text,
            'date_sold': date_tag.get_text(strip=True) if date_tag else ''
        })
    
  return pd.DataFrame(listings)