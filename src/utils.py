import pandas as pd
import os

def process_ebay_response(response, search_term):
    items = response.get('itemSummaries', [])
    if not items:
        return pd.DataFrame()
    
    return pd.DataFrame([{
        'title': item.get('title', ''),
        'price': float(item['price'].get('value', 0)),
        'condition': item.get('condition', 'N/A'),#if the item has no condition field, mark as 'N/A'.
        'url': item.get('itemWebUrl'),
        'search_term': search_term.lower()
    } for item in items])

def filter_outliers_group(group, column='price'):
    if len(group) < 5:  # Don't filter small groups
        return group
        
    q1 = group[column].quantile(0.25)  
    q3 = group[column].quantile(0.75)  
    iqr = q3 - q1
    lower_bound = q1 - 1 * iqr
    upper_bound = q3 + 1 * iqr
    return group[(group[column] >= lower_bound) & (group[column] <= upper_bound)]

def generate_aggregation(df, filter_extremes=True):
    if df.empty:
        return pd.DataFrame()
    line_width = 40
    print("\n=== ALL RAW LISTINGS ===".center(line_width))
    print(df[['condition', 'price']].sort_values('price').to_string(index=False))
    
    if filter_extremes:
        original_count = len(df)
        original_prices = df['price'].copy()
        original_index = df.index
        
        # nothing valid is accidentally excluded just because it lacks a condition / we apply a filter (N/A) 
        filtered_df = df.groupby('condition').apply(filter_outliers_group)
        
        # "useless" extra index level not important enough to display, comes with using groupby().apply()
        filtered_df = filtered_df.reset_index(level=0, drop=True)
        
        removed = original_count - len(filtered_df)
        print(f"\n=== REMOVED {removed} UNREALISTIC PRICES ===".center(line_width))
        
        # Find removed indices by comparing original and filtered
        removed_indices = original_index.difference(filtered_df.index)
        removed_prices = original_prices.loc[removed_indices]
        
        if not removed_prices.empty:
            print(pd.DataFrame({'price': removed_prices}).sort_values('price').to_string(index=False))
        else:
            print("(No extreme prices found)")
        
        print(f"\n=== FINAL {len(filtered_df)} REALISTIC LISTINGS ===".center(line_width))
        print(filtered_df[['condition', 'price']].sort_values('price').to_string(index=False))
        
        df = filtered_df  # Use filtered data for aggregation
    
    agg_df = df.groupby('condition').agg(
        count=('price', 'count'),
        min=('price', 'min'),
        max=('price', 'max'),
        mean=('price', 'mean'),
        median=('price', 'median')
    ).round(2)
    
    return agg_df
def save_data(df, search_term, google_sheets=False):
    os.makedirs('data', exist_ok=True)
    filename = f'data/{search_term.replace(" ", "_")}.csv'
    df.to_csv(filename, index=False)
    return filename