
import requests
from bs4 import BeautifulSoup

# Bright Data Web Unlocker credentials
PROXY = "brd.superproxy.io:33335"
PROXY_USER = "brd-customer-hl_f62a16b7-zone-wrapped"
PROXY_PASSWORD = "m6bkdb2u0147"

proxies = {
    "http": f"http://{PROXY_USER}:{PROXY_PASSWORD}@{PROXY}",
    "https": f"http://{PROXY_USER}:{PROXY_PASSWORD}@{PROXY}",
}

def fetch_amazon_page(isbn):
    """Fetch the Amazon product page for a given ISBN."""
    base_url = "https://www.amazon.com/s"
    params = {"k": isbn}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }

    print(f"Searching for ISBN: {isbn}...")
    try:
        response = requests.get(base_url, params=params, headers=headers, proxies=proxies, verify=False)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        product_link_tag = soup.find("a", class_="a-link-normal s-no-outline")
        if not product_link_tag:
            print(f"No product link found for ISBN {isbn}")
            return None

        product_url = "https://www.amazon.com" + product_link_tag['href']
        print(f"Product URL found: {product_url}")

        product_response = requests.get(product_url, headers=headers, proxies=proxies, verify=False)
        product_response.raise_for_status()
        return BeautifulSoup(product_response.text, 'html.parser')
    except Exception as e:
        print(f"Error fetching page for ISBN {isbn}: {e}")
        return None

def get_book_weight(soup):
    """Extract book weight from the product details section."""
    try:
        detail_div = soup.find('div', id='detailBulletsWrapper_feature_div')
        if detail_div:
            detail_list = detail_div.find_all('span', class_='a-list-item')
            for item in detail_list:
                if 'Item Weight' in item.text:
                    weight = item.text.split(':')[-1].strip()
                    print(f"Debug: Extracted book weight: {weight}")
                    return weight
        return None
    except Exception as e:
        print(f"Error extracting book weight: {e}")
        return None

def get_page_count(soup):
    """Extract page count from the product details section."""
    try:
        detail_div = soup.find('div', id='detailBulletsWrapper_feature_div')
        if detail_div:
            detail_list = detail_div.find_all('span', class_='a-list-item')
            for item in detail_list:
                if 'Paperback' in item.text and 'pages' in item.text:
                    raw_text = item.text.split(':')[-1].strip()
                    cleaned_text = ''.join(filter(str.isdigit, raw_text))  # Keep only numeric characters
                    page_count = int(cleaned_text)
                    print(f"Debug: Extracted page count: {page_count}")
                    return page_count
        return None
    except Exception as e:
        print(f"Error extracting page count: {e}")
        return None

def process_books(file_path):
    """Process a CSV of books to extract weight and page count using ISBN."""
    import pandas as pd  # Ensure Pandas is imported

    print("Loading the dataset...")
    books_data = pd.read_csv(file_path)
    print(f"Dataset loaded with {len(books_data)} records.")

    # Filter books with non-null ISBNs
    books_with_isbn = books_data[books_data['ISBN'].notnull()]
    print(f"Found {len(books_with_isbn)} books with valid ISBNs.")

    weights = []
    page_counts = []
    for index, row in books_with_isbn.iterrows():
        print(f"Processing book: {row['Title']} by {row['Author']}")
        soup = fetch_amazon_page(row['ISBN'])
        if soup:
            weight = get_book_weight(soup)
            page_count = get_page_count(soup)
            print(f"Debug: For ISBN {row['ISBN']}, Weight: {weight}, Page Count: {page_count}")
            weights.append(weight if weight else "N/A")
            page_counts.append(page_count if page_count else "N/A")
        else:
            print(f"Failed to fetch data for ISBN {row['ISBN']}")
            weights.append("N/A")
            page_counts.append("N/A")

    books_with_isbn['Weight'] = weights
    books_with_isbn['Page Count'] = page_counts

    output_path = "books_with_weight_and_page_count.csv"
    books_with_isbn.to_csv(output_path, index=False)
    print(f"Processed data saved to: {output_path}")
    
# Example file path to your CSV
input_file_path = "2024BookList.csv"

# Uncomment the following line to run the processing
process_books(input_file_path)
