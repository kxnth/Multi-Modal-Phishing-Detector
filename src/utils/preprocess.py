import pandas as pd
import re
from bs4 import BeautifulSoup
import os

# Remove HTML tags and replace URLs with a placeholder
def clean_email_text(raw_text):
    if not isinstance(raw_text, str):
        return ""
    
    text_no_html = BeautifulSoup(raw_text, "html.parser").get_text(separator=" ")
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    text_clean_urls = re.sub(url_pattern, '[URL]', text_no_html)
    clean_text = re.sub(r'\s+', ' ', text_clean_urls)
    return clean_text.strip()

safe_csv = "data/text/safe_email.csv"
phishing_csv = "data/text/phishing_emails.csv"
output_csv = "data/text/cleaned_emails.csv"

if os.path.exists(safe_csv) and os.path.exists(phishing_csv):
    print("Loading data...")
    
    df_safe = pd.read_csv(safe_csv)
    df_phish = pd.read_csv(phishing_csv)
    
    # Standardize column names across different data sources
    for df in [df_safe, df_phish]:
        if 'Email Text' in df.columns:
            df.rename(columns={'Email Text': 'text'}, inplace=True)
        elif 'Message' in df.columns:
            df.rename(columns={'Message': 'text'}, inplace=True)
        elif 'text' not in df.columns:
            df.rename(columns={df.columns[0]: 'text'}, inplace=True)

    df_safe['label'] = 0
    df_phish['label'] = 1
    
    # Combine safe and phishing emails into one dataset
    df_combined = pd.concat([df_safe[['text', 'label']], df_phish[['text', 'label']]], ignore_index=True)
    df_combined = df_combined.dropna()
    
    print("Cleaning text data...")
    df_combined['text'] = df_combined['text'].apply(clean_email_text)
    
    df_combined.to_csv(output_csv, index=False)
    print(f"Cleaned dataset saved. Total emails: {len(df_combined)}")

else:
    print("Error: Could not find files.")