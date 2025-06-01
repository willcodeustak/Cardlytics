import pandas as pd
import os

def process_ebay_response(response, search_term):
    items = response.get('itemSummaries', [])
    if not items:
        return pd.DataFrame()
    
    return pd.DataFrame([{
        'title': item.get('title', ''),
        'price': float(item['price'].get('value', 0)),
        'condition': item.get('condition', 'N/A'),
        'url': item.get('itemWebUrl'),
        'search_term': search_term.lower()
    } for item in items])

def generate_aggregation(df):
    if df.empty:
        return pd.DataFrame()
    
    return df.groupby('condition').agg({
        #i would do lowest, highest and average for user intuitive naming convention here but pandas does not allow
        'price': ['count', 'min', 'max', 'mean']
    }).round(2)

def save_data(df, search_term, google_sheets=False):
    os.makedirs('data', exist_ok=True)
    filename = f'data/{search_term.replace(" ", "_")}.csv'
    df.to_csv(filename, index=False)
    return filename