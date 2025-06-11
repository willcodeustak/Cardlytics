# src/utils.py
import pandas as pd
import os

def process_ebay_response(response, search_term):
    items = response.get('itemSummaries', [])
    if not items:
        return pd.DataFrame() #pandas syntax - bypass error if (!items)
    
    return pd.DataFrame([{     #only query things we care about
        'title': item.get('title', ''),
        'price': float(item['price'].get('value', 0)),
        'condition': item.get('condition', 'N/A'),
        'url': item.get('itemWebUrl'),
        'search_term': search_term.lower()
    } for item in items])

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Note: Future Warning - DataFrameGroupBy.apply operated on the grouping columns. This behavior is deprecated, and in a future version of pandas the grouping columns will be excluded from the operation. Either pass `include_groups=False` to exclude the groupings or explicitly select the grouping columns after groupby to silence this warning.
  filtered_df = df.groupby('condition', group_keys=False).apply(filter_outliers_group)
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def filter_outliers_group(group, column='price'):
    if len(group) < 5: #too small for outlier check
        return group
    #(IQR) 

    q1 = group[column].quantile(0.25)  
    q3 = group[column].quantile(0.75)  
    iqr = q3 - q1

    # range of acceptance for filtering outliers 
    lower_bound = q1 - 1 * iqr
    upper_bound = q3 + 1 * iqr

    #only want data that is within bounds
    return group[(group[column] >= lower_bound) & (group[column] <= upper_bound)]

def generate_aggregation(df, filter_extremes=True):
    if df.empty:
        return pd.DataFrame()
    
    line_width = 40
    print(f"Fetched {len(df)} listings")
    print("\n=== ALL RAW LISTINGS ===".center(line_width))
    print(df[['condition', 'price']].sort_values('price').to_string(index=False))
    
    if filter_extremes: 
        filtered_df = df.groupby('condition', group_keys=False).apply(filter_outliers_group)
        removed = len(df) - len(filtered_df)
        
        print(f"\n=== REMOVED {removed} UNREALISTIC PRICES ===".center(line_width))
        removed_prices = df[~df.index.isin(filtered_df.index)]['price']
        print(pd.DataFrame({'price': removed_prices}).sort_values('price').to_string(index=False) if not removed_prices.empty else "(No extreme prices found)")
        
        print(f"\n=== FINAL {len(filtered_df)} REALISTIC LISTINGS ===".center(line_width))
        print(filtered_df[['condition', 'price']].sort_values('price').to_string(index=False))
        df = filtered_df
    

    #main aggregation seperated by condition
    agg_df = df.groupby('condition').agg(
        count=('price', 'count'),
        min=('price', 'min'),
        max=('price', 'max'),
        mean=('price', 'mean'),
        median=('price', 'median')
    ).round(2)
    
    return agg_df

def save_data(df, search_term, google_sheets=False):
    if df.empty:
        return "No data to save"
#excel files currently broken
    excel_filename = f"{search_term.replace(' ', '_')}_prices.xlsx"
    df.to_excel(excel_filename, index=False)
    
    if not google_sheets:
        return excel_filename

    try: #google stuff
        from google.oauth2 import service_account
        import gspread
        
        CREDS_PATH = '/app/src/google_credentials.json' 
        
        # Define api ussage
        SCOPE = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = service_account.Credentials.from_service_account_file(
            CREDS_PATH, scopes=SCOPE)
        
        gc = gspread.authorize(creds)
        
        # create a new sheet
        sheet_name = f"Pokemon - {search_term[:50]}"
        try:
            sheet = gc.open(sheet_name).sheet1
        except gspread.SpreadsheetNotFound:
            sheet = gc.create(sheet_name).sheet1
        
  
        SHARE_EMAIL = os.getenv('GOOGLE_SHEETS_SHARE_EMAIL')
        try:
            sheet.spreadsheet.share(SHARE_EMAIL, perm_type='user', role='writer', email_message='Here is the Pokemon card pricing data you requested')
            print(f"Shared with your email")
        except Exception as share_error:
            print(f"Sharing failed: {share_error}")
        #might not be working as intended, opens a new sheet everytime instead of clearing.
        sheet.clear()
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
        
        print(f"\nSuccess! Google Sheet created: {sheet.spreadsheet.url}")
        return sheet.spreadsheet.url
        
    except Exception as e:
        print(f"\nGoogle Sheets Error: {str(e)}")
        print("Falling back to local Excel file")
        return excel_filename