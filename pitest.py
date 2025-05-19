import openai
import pandas as pd
import time

# Load the dataset
file_path = '2024-Wrapped_updated.csv'
books_df = pd.read_csv(file_path)

# Add a column for dimensions if it doesn't exist
if 'Dimensions' not in books_df.columns:
    books_df['Dimensions'] = None

# Set your OpenAI API key
openai.api_key = "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"

# Define a function to query OpenAI for book dimensions
def get_book_dimensions_via_openai(title, author):
    try:
        # Create a prompt to ask for dimensions
        prompt = f"Provide the physical dimensions (height, width, and thickness in inches) for the book '{title}' by {author}. If exact dimensions aren't available, give an approximate range."
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        dimensions = response['choices'][0]['message']['content'].strip()
        print(f"Dimensions for '{title}' by {author}: {dimensions}")
        return dimensions
    
    except Exception as e:
        print(f"Error fetching dimensions for '{title}' by {author}: {e}")
        return None

# Iterate through the dataset and fetch dimensions for each book
for index, row in books_df.iterrows():
    if pd.isna(row['Dimensions']):  # Only fetch if dimensions are missing
        title = row['Title']
        author = row['Author']
        print(f"Fetching dimensions for '{title}' by {author}...")
        dimensions = get_book_dimensions_via_openai(title, author)
        books_df.at[index, 'Dimensions'] = dimensions
        time.sleep(1)  # Add a small delay to avoid hitting API rate limits

# Save the updated dataset to a new CSV
output_file_path = '2024-Wrapped_with_dimensions_openai.csv'
books_df.to_csv(output_file_path, index=False)

print(f"Updated dataset saved to {output_file_path}")