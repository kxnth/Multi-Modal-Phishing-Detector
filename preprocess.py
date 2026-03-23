import pandas as pd

df = pd.read_csv("emails.csv")

df = df.rename(columns={'Email Text': 'text', 'Email Type': 'label'})

df['label'] = df['label'].map({'Phishing Email': 1, 'Safe Email': 0})

df = df[['text', 'label']].dropna()
df.to_csv("cleaned_emails.csv", index=False)

print(f"Dataset cleaned and saved. Total valid emails: {len(df)}")