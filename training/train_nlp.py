import pandas as pd
import torch
import re
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import numpy as np
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import Trainer, TrainingArguments
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import warnings
warnings.filterwarnings("ignore")

# Normalize text to lowercase and count URLs as a phishing indicator
def clean_text(text):
    text = str(text).lower()
    urls = len(re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text))
    return f"[urls:{urls}] {text}"

# Container for tokenized emails and their labels
class EmailDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings 
        self.labels = labels       
        
    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item

    def __len__(self):
        return len(self.labels)

# Calculate model performance metrics: accuracy, precision, recall, and F1 score
def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def train_tutorial_model():
    # Load the main dataset and standardize column names
    print("Loading dataset...")
    try:
        df = pd.read_csv("dataset/text/phishing_email.csv")
        
        if 'Email Text' in df.columns:
            df.rename(columns={'Email Text': 'text'}, inplace=True)
        if 'Email Type' in df.columns:
            df.rename(columns={'Email Type': 'label'}, inplace=True)
            if df['label'].dtype == object:
                df['label'] = df['label'].apply(lambda x: 1 if 'Phish' in str(x) else 0)
    except FileNotFoundError:
        df_safe = pd.read_csv("dataset/text/safe_email.csv")
        df_phish = pd.read_csv("dataset/text/phishing_emails.csv")
        
        for d in [df_safe, df_phish]:
            if 'Email Text' in d.columns: d.rename(columns={'Email Text': 'text'}, inplace=True)
            elif 'Message' in d.columns: d.rename(columns={'Message': 'text'}, inplace=True)
            elif 'text' not in d.columns: d.rename(columns={d.columns[0]: 'text'}, inplace=True)
                
        df_safe['label'] = 0
        df_phish['label'] = 1
        df = pd.concat([df_phish, df_safe], ignore_index=True)

    if 'text' not in df.columns:
        df.rename(columns={df.columns[0]: 'text'}, inplace=True)

    # Remove empty rows and limit to 15,000 emails
    df.dropna(subset=['text'], inplace=True)
    df['label'] = pd.to_numeric(df['label'], errors='coerce').fillna(0).astype(int)
    df = df.sample(n=min(15000, len(df)), random_state=42).reset_index(drop=True)
    
    # Clean the text using our cleanup function.
    print("Preprocessing text...")
    df['text'] = df['text'].apply(clean_text)

    # Split the dataset into training (70%), validation (10%), and test (20%) sets
    train_val_texts, test_texts, train_val_labels, test_labels = train_test_split(
        df['text'].tolist(), df['label'].tolist(), test_size=0.2, random_state=42, stratify=df['label']
    )
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        train_val_texts, train_val_labels, test_size=0.125, random_state=42, stratify=train_val_labels
    )

    os.makedirs("dataset/splits", exist_ok=True)
    pd.DataFrame({"text": test_texts, "label": test_labels}).to_csv("dataset/splits/test_set.csv", index=False)

    # Translate the text into numerical IDs that the AI can process
    print("Tokenizing with BERT-Tiny...")
    model_name = "prajjwal1/bert-tiny"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)

    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=256)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=256)

    train_dataset = EmailDataset(train_encodings, train_labels)
    val_dataset = EmailDataset(val_encodings, val_labels)

    # Setting the instructions for the training process
    training_args = TrainingArguments(
        output_dir='./results_nlp',
        eval_strategy="epoch",             
        save_strategy="epoch",             
        save_total_limit=2,                
        learning_rate=2e-5,                
        per_device_train_batch_size=16,    
        per_device_eval_batch_size=16,     
        num_train_epochs=5,                
        weight_decay=0.01,                 
        optim="adamw_torch",               
        logging_dir='./logs',
        logging_strategy="epoch",          
        load_best_model_at_end=True,       
        metric_for_best_model="f1",        
        greater_is_better=True,
        fp16=torch.cuda.is_available()     
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics
    )

    # Begin the learning process
    print("Starting Training...")
    trainer.train() 

    # Save the finished AI brain to use later.
    print("Saving the Final Model & Tokenizer...")
    os.makedirs("models/nlp_model_bert", exist_ok=True)
    trainer.save_model("models/nlp_model_bert")
    tokenizer.save_pretrained("models/nlp_model_bert")
    print("Training Complete!")

if __name__ == "__main__":
    train_tutorial_model()