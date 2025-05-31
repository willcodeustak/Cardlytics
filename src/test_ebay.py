from ebay_scraper import parse_ebay_html
from utils import fetch_ebay_listings
import pandas as pd

# Test eBay search
search_term = "pikachu"
sold_only = True  # False for current listings

# Fetch live data from eBay
html_content = fetch_ebay_listings(search_term, sold_items=sold_only)

if html_content:
    df = parse_ebay_html(html_content)
    
    #Clean and display results
    if not df.empty:
        df = df[~df['price'].str.contains('to', na=False)]
        df['price'] = df['price'].str.replace(r'[^\d.]', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df = df.dropna(subset=['price'])
        
        print(f"Found {len(df)} valid listings")
        print(df.head())
        print(f"\nAverage price: ${df['price'].mean():.2f}")
    else:
        print("No listings found in the parsed data")
else:
    print("Failed to fetch eBay data")