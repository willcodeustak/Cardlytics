import re
import pandas as pd
from bs4 import BeautifulSoup
from utils import fetch_ebay_listings, clean_prices, save_data

def parse_ebay_html(html):
    soup = BeautifulSoup(html, 'lxml')
    listings = []

    items = soup.find_all('li', {'class': 's-item'})
    print(f"Found {len(items)} items on the page.")  # extra logging

    for item in items:
        # Extract the price text, skip if missing
        price_tag = item.find('span', {'class': 's-item__price'})
        if not price_tag:
            continue
        price_text = price_tag.get_text(strip=True)
        # Remove currency symbols/prefix like 'US $'
        price_text = re.sub(r'^[A-Za-z$ ]+', '', price_text)

        title_tag = item.find('h3', {'class': 's-item__title'})
        title = title_tag.get_text(strip=True) if title_tag else ''

        date_tag = item.find('span', {'class': 's-item__title--tagblock'})
        date_sold = date_tag.get_text(strip=True) if date_tag else ''

        listings.append({
            'title': title,
            'price': price_text,
            'date_sold': date_sold
        })

    df = pd.DataFrame(listings)
    return df

def main():
    search_term = input("Enter Pokémon card to analyze (e.g. 'pikachu'): ").strip()
    if not search_term:
        print("Search term cannot be empty.")
        return

    sold_only = input("Analyze sold items only? (y/n): ").strip().lower() == 'y'

    print(f"Fetching {'sold' if sold_only else 'current'} listings for '{search_term}'...")
    html = fetch_ebay_listings(search_term, sold_items=sold_only)
    if not html:
        print("No data fetched.")
        return

    df = parse_ebay_html(html)
    if df.empty:
        print("No listings found.")
        return

    df = clean_prices(df)
    if df.empty:
        print("No valid prices found after cleaning.")
        return

    print(f"Found {len(df)} listings with prices.")
    print(f"Average price: ${df['price'].mean():.2f}")
    print(f"Lowest price: ${df['price'].min():.2f}")
    print(f"Highest price: ${df['price'].max():.2f}")

    save_data(df, search_term)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
            print("\nProcess interrupted by user.")