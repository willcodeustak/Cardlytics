from ebayApi import EBayAPI
from utils import process_ebay_response, save_data

def main():
    api = EBayAPI()
    search_term = input("Enter Pokémon card name: ").strip()
    sold_only = input("Sold items only? (y/n): ").lower() == 'y'
    
    data = api.search_items(search_term, sold_only)
    df = process_ebay_response(data)
    
    if not df.empty:
        filename = save_data(df, search_term)
        print(f"✅ Saved {len(df)} listings to {filename}")
        print(df[['title', 'price']].head())
    else:
        print("❌ No results found")

if __name__ == "__main__":
    main()