import pandas as pd

df = pd.read_csv("emails.csv")

# Rename columns to match rubric requirements
df = df.rename(columns={'Email Text': 'text', 'Email Type': 'label'})

# Convert text labels to binary (1 = phishing, 0 = safe)
df['label'] = df['label'].map({'Phishing Email': 1, 'Safe Email': 0})

# Keep only necessary columns and drop empty rows
df = df[['text', 'label']].dropna()
df.to_csv("cleaned_emails.csv", index=False)

print(f"Dataset cleaned and saved. Total valid emails: {len(df)}")