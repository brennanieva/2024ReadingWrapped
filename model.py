import pandas as pd
from huggingface_hub import InferenceClient

# Load your dataset
file_path = "2024-Wrapped - full_2024.csv"
data = pd.read_csv(file_path)

print(f"Dataset loaded successfully. Total records: {len(data)}")
print("Dataset Columns:", data.columns)

# Set up Hugging Face API
# Replace with your actual Hugging Face API token
huggingface_token = "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"
model_id = "google/flan-t5-large"

# Initialize the Hugging Face Inference Client
inference = InferenceClient(model=model_id, token=huggingface_token)
print("Hugging Face API initialized.")

# Function to get genre and subgenre
def get_genre_and_subgenre_hub(title, description):
    prompt = f"""Classify the following book:
    Title: {title}
    Description: {description}
    Provide the output in this format:
    Genre: [Genre]
    Subgenre: [Subgenre]"""
    try:
        # Call the Hugging Face Inference API using the `post` method
        response = inference.post(prompt)
        
        # Parse the response
        if isinstance(response, dict) and "generated_text" in response:
            output = response["generated_text"].strip()
        elif isinstance(response, str):
            output = response.strip()
        else:
            raise ValueError("Unexpected response format from API.")

        # Split the output into lines
        return output.splitlines()
    except Exception as e:
        print(f"Error for title '{title}': {e}")
        return ["Genre: Unknown", "Subgenre: Unknown"]

# Add Genre and Subgenre columns to the dataset
data['Genre'] = ""
data['Subgenre'] = ""

print("Columns for Genre and Subgenre added to the dataset.")

# Process each row in the dataset
for index, row in data.iterrows():
    title = row.get('Title', "")  # Use 'Title' as the correct column name
    description = row.get('Comments', "")  # Use 'Comments' as the correct column name

    # Skip processing if no title or description
    if not title or not description:
        print(f"Skipping row {index}: Missing title or description.")
        continue

    # Get genre and subgenre
    print(f"Processing row {index}: Title = {title}")
    genre_info = get_genre_and_subgenre_hub(title, description)

    # Update the dataframe
    if genre_info and len(genre_info) >= 2:
        data.at[index, 'Genre'] = genre_info[0].split(": ")[1] if ": " in genre_info[0] else "Unknown"
        data.at[index, 'Subgenre'] = genre_info[1].split(": ")[1] if ": " in genre_info[1] else "Unknown"
        print(f"Row {index} processed successfully: Genre = {data.at[index, 'Genre']}, Subgenre = {data.at[index, 'Subgenre']}")
    else:
        print(f"Row {index} could not be classified.")

# Save the updated dataset
output_file = "2024-Wrapped_with_Genres_HuggingFace.csv"
data.to_csv(output_file, index=False)

# Print a summary of the processed data
print("Sample of updated data:")
print(data[['Title', 'Genre', 'Subgenre']].head())

print(f"Processing completed. Updated dataset saved to {output_file}.")