import pandas as pd
import requests

# Load the dataset
file_path = "2024-Wrapped_updated.csv"
books_df = pd.read_csv(file_path)

# Add new columns if not already present
if 'Thickness (cm)' not in books_df.columns:
    books_df['Thickness (cm)'] = None
if 'USD Sale Price' not in books_df.columns:
    books_df['USD Sale Price'] = None
if 'Main Category' not in books_df.columns:
    books_df['Main Category'] = None
if 'Categories' not in books_df.columns:
    books_df['Categories'] = None

# Google Books API setup
API_KEY = 'AIzaSyAXSe4eIHocSZOtAN5CYfuu5oxTl6FP0KM'
BASE_URL = 'https://www.googleapis.com/books/v1/volumes'

def get_additional_book_details(title, author=None):
    """Fetch thickness, sale price, main category, and categories from Google Books API."""
    params = {'q': f'intitle:{title}', 'key': API_KEY, 'maxResults': 1}
    if author:
        params['q'] += f'+inauthor:{author}'
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            volume_info = data['items'][0].get('volumeInfo', {})
            sale_info = data['items'][0].get('saleInfo', {})
            
            # Extract thickness
            dimensions = volume_info.get('dimensions', {})
            thickness = dimensions.get('thickness')
            if thickness and "cm" in thickness:
                thickness = float(thickness.replace(" cm", ""))
            elif thickness:
                print(f"Unexpected format for thickness: {thickness}")
                thickness = None
            
            # Extract USD sale price
            usd_price = None
            if sale_info.get('listPrice') and sale_info['listPrice'].get('currencyCode') == 'USD':
                usd_price = sale_info['listPrice'].get('amount')
            
            # Extract main category and categories
            main_category = volume_info.get('mainCategory')
            categories = volume_info.get('categories')
            
            return thickness, usd_price, main_category, categories
    return None, None, None, None

# Update only the specific columns
print("Fetching additional details (thickness, sale price, main category, categories) from Google Books API...")
for idx, row in books_df.iterrows():
    if pd.notnull(row['Thickness (cm)']) and pd.notnull(row['USD Sale Price']) and pd.notnull(row['Main Category']) and pd.notnull(row['Categories']):
        continue  # Skip rows already filled
    
    title = row['Title']  # Replace with the actual column name for book titles
    author = row.get('Author')  # Replace with the actual column name for authors (if available)
    print(f"Processing book: {title} (Author: {author})")
    
    thickness, usd_price, main_category, categories = get_additional_book_details(title, author)
    
    # Update the dataset with retrieved details
    books_df.at[idx, 'Thickness (cm)'] = thickness
    books_df.at[idx, 'USD Sale Price'] = usd_price
    books_df.at[idx, 'Main Category'] = main_category
    books_df.at[idx, 'Categories'] = ', '.join(categories) if categories else None
    
    print(f"  - Thickness: {thickness} cm")
    print(f"  - USD Sale Price: {usd_price}")
    print(f"  - Main Category: {main_category}")
    print(f"  - Categories: {', '.join(categories) if categories else 'Not Available'}")

print("Fetching complete. Saving updated dataset...")

# Save the updated dataset
output_path = "2024-Wrapped_updated.csv"
books_df.to_csv(output_path, index=False)
print(f"Updated dataset saved to {output_path}")