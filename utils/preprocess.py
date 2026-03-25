import pandas as pd
import re
from bs4 import BeautifulSoup
import os

def clean_email_text(raw_text):
    if not isinstance(raw_text, str):
        return ""
    # 1. Strip HTML tags
    text_no_html = BeautifulSoup(raw_text, "html.parser").get_text(separator=" ")
    # 2. Clean URLs (replace with [URL])
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    text_clean_urls = re.sub(url_pattern, '[URL]', text_no_html)
    # 3. Clean weird characters
    clean_text = re.sub(r'\s+', ' ', text_no_html)
    return clean_text.strip()

# Your specific filenames
safe_csv = "dataset/text/safe_email.csv"
phishing_csv = "dataset/text/phishing_emails.csv"
output_csv = "dataset/text/cleaned_emails.csv"

if os.path.exists(safe_csv) and os.path.exists(phishing_csv):
    print("Found both CSV files. Loading data...")
    
    # Load the datasets
    df_safe = pd.read_csv(safe_csv)
    df_phish = pd.read_csv(phishing_csv)
    
    # Kaggle datasets name their columns differently (e.g., 'Message', 'Email Text', or just 'text').
    # This forces whatever the text column is named to be standard 'text'.
    for df in [df_safe, df_phish]:
        if 'Email Text' in df.columns:
            df.rename(columns={'Email Text': 'text'}, inplace=True)
        elif 'Message' in df.columns:
            df.rename(columns={'Message': 'text'}, inplace=True)
        elif 'text' not in df.columns:
            # If we can't find the name, just grab the first column
            df.rename(columns={df.columns[0]: 'text'}, inplace=True)

    # Label them strictly for the BERT model: 0 is Safe, 1 is Phishing
    df_safe['label'] = 0
    df_phish['label'] = 1
    
    # Smash them together into one dataframe
    df_combined = pd.concat([df_safe[['text', 'label']], df_phish[['text', 'label']]], ignore_index=True)
    df_combined = df_combined.dropna()
    
    print("Stripping HTML and cleaning URLs (this might take a few seconds)...")
    df_combined['text'] = df_combined['text'].apply(clean_email_text)
    
    # Save the master file that evaluate_models.py is looking for
    df_combined.to_csv(output_csv, index=False)
    print(f"✅ Step 2 Complete! Cleaned dataset saved. Total valid emails ready for AI: {len(df_combined)}")

else:
    print("Error: Could not find one or both of the files. Please check the filenames:")
    if not os.path.exists(safe_csv): print(f"❌ Missing: {safe_csv}")
    if not os.path.exists(phishing_csv): print(f"❌ Missing: {phishing_csv}")