# src/main.py
from ebayApi import EBayAPI
from utils import process_ebay_response, save_data, generate_aggregation
from dotenv import load_dotenv 
load_dotenv()

def main():
    api = EBayAPI()
    
    print("=== Pokémon Card Price Checker ===")

    search_term = input("Enter Pokémon card name: ").strip()
    card_number = input("Enter card number if known (or press Enter): ").strip()
    sold_only = input("Sold items only? (y/n): ").lower() == 'y'
    use_google = input("Save to Google Sheets? (y/n): ").lower() == 'y'
    #query for search parameters
    data = api.search_items(search_term, card_number if card_number else None, sold_only)
    df = process_ebay_response(data, search_term)
    
    if not df.empty:
        #if user selects yes we save fetched listings on google sheets
        save_data(df, search_term, google_sheets=use_google) 
                
        agg_df = generate_aggregation(df) #avg, min, max price
        print("\n=== Price Summary ===") 
        print(agg_df.to_string(index=False))#remove index numbering (cleaner ui purposes)
    else:
        print("No results found")

if __name__ == "__main__":
    main()