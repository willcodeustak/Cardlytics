import os
import pandas as pd

def process_ebay_response(response):
    """Convert API JSON to clean DataFrame"""
    items = response.get('itemSummaries', [])
    return pd.DataFrame([{
        'title': item.get('title'),
        'price': item['price'].get('value'),
        'condition': item.get('condition', 'N/A'),
        'sold_date': item.get('soldDate', ''),
        'url': item.get('itemWebUrl')
    } for item in items])

def save_data(df, search_term):
    """Save DataFrame to CSV"""
    os.makedirs('data', exist_ok=True)
    filename = f'data/{search_term.replace(" ", "_")}_prices.csv'
    df.to_csv(filename, index=False)
    return filename