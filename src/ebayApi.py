import os
import requests
from dotenv import load_dotenv
from config import EBAY_API_URL, MARKETPLACE_ID

load_dotenv()

class EBayAPI:
    def __init__(self):
        self.oauth_token = os.getenv("EBAY_OAUTH_TOKEN")
    
    def search_items(self, query, sold_only=False, limit=50):
        headers = {
            "Authorization": f"Bearer {self.oauth_token}",
            "X-EBAY-C-MARKETPLACE-ID": MARKETPLACE_ID
        }
        params = {
            "q": query,
            "limit": limit,
            "filter": "soldItemsOnly:true" if sold_only else ""
        }
        
        response = requests.get(EBAY_API_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json()