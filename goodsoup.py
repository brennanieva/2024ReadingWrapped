import requests
from bs4 import BeautifulSoup
import pandas as pd  # Ensure Pandas is imported
import time

# Bright Data Web Unlocker credentials
PROXY = "brd.superproxy.io:33335"
PROXY_USER = "brd-customer-hl_f62a16b7-zone-wrapped"
PROXY_PASSWORD = "m6bkdb2u0147"

proxies = {
    "http": f"http://{PROXY_USER}:{PROXY_PASSWORD}@{PROXY}",
    "https": f"http://{PROXY_USER}:{PROXY_PASSWORD}@{PROXY}",
}

def get_amazon_dimensions(isbn):
    """
    Scrape book dimensions from the first Amazon search result using ISBN.
    """
    base_url = "https://www.amazon.com/s"
    params = {"k": isbn}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }
    
    print(f"Searching for ISBN: {isbn}...")
    try:
        # Step 1: Search for the book on Amazon using Bright Data's proxy
        response = requests.get(base_url, params=params, headers=headers, proxies=proxies, verify=False)
        response.raise_for_status()
        print(f"Search results fetched for ISBN: {isbn}")
        
        # Step 2: Parse search results
        soup = BeautifulSoup(response.text, 'html.parser')
        product_link_tag = soup.find("a", class_="a-link-normal s-no-outline")
        if not product_link_tag:
            print(f"No product link found for ISBN {isbn}")
            return "No product link found"
        
        product_url = "https://www.amazon.com" + product_link_tag['href']
        print(f"Product URL found: {product_url}")

        # Step 3: Fetch product details using Bright Data's proxy
        product_response = requests.get(product_url, headers=headers, proxies=proxies, verify=False)
        product_response.raise_for_status()
        print(f"Fetched product details for ISBN: {isbn}")
        
        product_soup = BeautifulSoup(product_response.text, 'html.parser')

        # Step 4: Locate the dimensions in the "rich_product_information" section
        rich_info_section = product_soup.find("div", id="rich_product_information")
        if rich_info_section:
            dimensions_card = rich_info_section.find("div", id="rpi-attribute-book_details-dimensions")
            if dimensions_card:
                dimensions_value = dimensions_card.find("div", class_="rpi-attribute-value")
                if dimensions_value:
                    dimensions = dimensions_value.get_text(strip=True)
                    print(f"Dimensions found: {dimensions}")
                    return dimensions

        print(f"No dimensions found for ISBN {isbn}")
        return "Dimensions not found"
    except Exception as e:
        print(f"Error processing ISBN {isbn}: {e}")
        return f"Error: {e}"

def process_books(file_path):
    """
    Process a CSV of books, searching for dimensions on Amazon using ISBN.
    """
    print("Loading the dataset...")
    books_data = pd.read_csv(file_path)  # Ensure Pandas is used to read the dataset
    print(f"Dataset loaded with {len(books_data)} records.")

    # Filter books with non-null ISBNs
    books_with_isbn = books_data[books_data['ISBN'].notnull()]
    print(f"Found {len(books_with_isbn)} books with valid ISBNs.")

    # Apply the scraping function to each ISBN
    dimensions = []
    for index, row in books_with_isbn.iterrows():
        print(f"Processing book: {row['Title']} by {row['Author']}")
        dimensions.append(get_amazon_dimensions(row['ISBN']))
        time.sleep(2)  # Add delay to avoid unnecessary API usage

    books_with_isbn['Dimensions'] = dimensions

    # Save the results to a new CSV file
    output_path = "books_with_dimensions_bright_data.csv"
    books_with_isbn.to_csv(output_path, index=False)
    print(f"Processed data saved to: {output_path}")

# File path to your CSV
input_file_path = "2024-Wrapped_updated.csv"

# Run the processing
process_books(input_file_path)