# src/utils.py

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
            response = requests.get(BASE_URL, headers=HEADERS, params=params)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                print("Failed after multiple attempts.")
                return None
            time.sleep(2 ** attempt + random.uniform(0, 1))

def clean_prices(df):
    df = df[~df['price'].str.contains('to', na=False)]
    df['price'] = df['price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.dropna(subset=['price'])
    return df

def save_data(df, search_term):
    os.makedirs('data', exist_ok=True)
    filename = f'data/{search_term.replace(" ", "_")}_prices.csv'
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
