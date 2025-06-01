import os
import requests
from config import EBAY_API_URL, MARKETPLACE_ID

class EBayAPI:
    def __init__(self):
        self.oauth_token = os.getenv("EBAY_OAUTH_TOKEN")
        if not self.oauth_token:
            raise ValueError("EBAY_OAUTH_TOKEN environment variable not set")
    
    def search_items(self, query, card_number=None, sold_only=False, limit=50):
        headers = {
            "Authorization": f"Bearer {self.oauth_token}",
            "X-EBAY-C-MARKETPLACE-ID": MARKETPLACE_ID,
        }
        
        search_query = query
        if card_number:
            search_query += f" {card_number}"
            
        params = {
            "q": search_query,
            "limit": limit,
            "filter": "soldItemsOnly:true" if sold_only else "",
            "category_ids": "183454"  # Pokémon TCG category
        }
        
        response = requests.get(EBAY_API_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json()