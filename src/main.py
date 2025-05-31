from ebay_scraper import parse_ebay_html
from pricecharting_scraper import fetch_pricecharting_data, parse_pricecharting_html
from utils import clean_prices, save_data, fetch_ebay_listings

def ebay_flow(search_term, sold_only):
    html = fetch_ebay_listings(search_term, sold_items=sold_only)
    return parse_ebay_html(html) if html else None

def pricecharting_flow(search_term):
    html = fetch_pricecharting_data(search_term)
    return parse_pricecharting_html(html) if html else None

def main():
    source = input("Which source? (eBay/PriceCharting): ").strip().lower()
    search_term = input("Enter Pokémon card name: ").strip()
    
    if source == 'ebay':
        sold_only = input("Sold items only? (y/n): ").strip().lower() == 'y'
        df = ebay_flow(search_term, sold_only)
    elif source == 'pricecharting':
        df = pricecharting_flow(search_term)
    else:
        print("Invalid source")
        return

    if df is None or df.empty:
        print("No valid data found")
        return

    df = clean_prices(df)
    filename = save_data(df, search_term)
    
    print(f"\nResults saved to {filename}")
    print(f"Found {len(df)} valid listings")
    if 'price' in df.columns:
        print(f"Average price: ${df['price'].mean():.2f}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled")