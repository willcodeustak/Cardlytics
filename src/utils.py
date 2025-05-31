import os
import time
import random
import requests
import pandas as pd
from config import BASE_URL, HEADERS

def fetch_ebay_listings(search_term, sold_items=False, retries=2):
    params = {
        "_nkw": search_term,
        "_sacat": 0,
        "_ipg": 50,
        "LH_Sold": 1 if sold_items else 0
    }
    for attempt in range(retries):
        try:
            response = requests.get(
                BASE_URL,
                headers=HEADERS,
                params=params,
                timeout=10 
            )
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == retries - 1:
                return None
            time.sleep(2 ** attempt + random.uniform(0, 1))

def clean_prices(df):
    if 'price' in df.columns:
        df = df[~df['price'].str.contains('to', na=False)]
        df['price'] = df['price'].str.replace(r'[^\d.]', '', regex=True)
    df = df.dropna(subset=df.columns.intersection(['price', 'mid_price']))
    return df

def save_data(df, search_term):
    os.makedirs('data', exist_ok=True)
    filename = f'data/{search_term.replace(" ", "_")}_prices.csv'
    df.to_csv(filename, index=False)
    return filename