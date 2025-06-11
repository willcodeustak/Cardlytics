from ebayApi import EBayAPI
from utils import process_ebay_response, save_data, generate_aggregation
# if not running on docker container - running python main.py instead
from dotenv import load_dotenv 
load_dotenv()

def main():
    api = EBayAPI()
    
    print("=== Pokémon Card Price Checker ===")
    search_term = input("Enter Pokémon card name: ").strip()
    card_number = input("Enter card number if known (or press Enter): ").strip()
    sold_only = input("Sold items only? (y/n): ").lower() == 'y'
    use_google = input("Save to Google Sheets? (y/n): ").lower() == 'y'
    
    data = api.search_items(search_term, card_number if card_number else None, sold_only)
    df = process_ebay_response(data, search_term)
    
    if not df.empty:
        output = save_data(df, search_term, google_sheets=use_google)
        print(f"Saved {len(df)} listings to {output}")
        
        agg_df = generate_aggregation(df)
        print("\n=== Price Summary ===")
        print(agg_df.to_string(index=False))
    else:
        print("No results found")

if __name__ == "__main__":
    main()