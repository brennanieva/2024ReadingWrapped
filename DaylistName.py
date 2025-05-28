import os
import pandas as pd
from pathlib import Path
import openai

# API Key Setup
openai_key = os.environ.get("OPENAI_API_KEY")
if not openai_key:
    raise RuntimeError("OPENAI_API_KEY not found.")

openai.api_key = openai_key

book_df = pd.read_csv("2024BookList.csv")

#Creating a filtered version of the BookList
filtered_df = book_df[['MonthRead', 'MonthName', 'Title', 'Tags']].dropna()




# Create book blurbs of tags for each month
month_blobs = {}
for month, group in filtered_df.groupby('MonthName'):
    blob = "\n".join(
        f"- {row['Title']}: {str(row['Tags'])[:100]}"
        for _, row in group.iterrows()
    )
    month_blobs[month] = blob

# Create OpenAI-style prompts
openai_prompts = []
for month, blob in month_blobs.items():
    month_tags = filtered_df[filtered_df['MonthName'] == month]['Tags'].dropna()
    top_tags = month_tags.value_counts().head(3).index.tolist()
    tags_str = ', '.join(top_tags)
    # Get the corresponding MonthRead value (assumes all rows for a month have the same MonthRead)
    month_read = filtered_df[filtered_df['MonthName'] == month]['MonthRead'].iloc[0]
    daylist_prompt = f"""Here are the books I read in {month} 2024:\n\n{blob}\n\nBased on this, give me a Spotify Daylist-style mood name. It should be 3 to 4 words followed by the month, lowercase, vibe-based, and playful.\nExample: 'melancholy vampire September', 'satire audiobook hour February', 'dreamcore whimsical deligh May'\n\n Please provide the mood name for {month} 2024"""
    openai_prompts.append({
        "MonthName": month,
        "MonthRead": month_read,
        "Daylist_Prompt": daylist_prompt,
    })

# Store prompt df
month_df = pd.DataFrame(openai_prompts, columns=["MonthName", "MonthRead", "Daylist_Prompt"])
month_df = month_df.sort_values(by='MonthRead').reset_index(drop=True)
# Add a column for books read count in each month
month_df["Books_Read"] = month_df["MonthName"].apply(
    lambda month: filtered_df[filtered_df['MonthName'] == month]['Title'].nunique()
)


# Function to get mood name from prompt using OpenAI, ChatGPT used to come up with a role 
def MonthReview(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative assistant for Spotify-style daylist mood naming and recommending books."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"


# Apply to each prompt and get Daylist mood names
month_df["Daylist_Name"] = month_df["Daylist_Prompt"].apply(MonthReview)



for index, row in month_df.iterrows():
    print("You had a {} in {} 2024 with {} books read.".format(
        row["Daylist_Name"],
        row["MonthName"],
        row["Books_Read"],
    ))


