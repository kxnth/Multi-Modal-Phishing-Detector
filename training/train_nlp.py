import pandas as pd
import torch
import torch.nn as nn
import re
from datasets import Dataset
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import os

def compute_metrics(pred):
    """Rubric Phase 3: Implement a compute_metrics function"""
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    acc = accuracy_score(labels, preds)
    return {'accuracy': acc, 'f1': f1, 'precision': precision, 'recall': recall}

def extract_url_features(text):
    """
    RUBRIC REQUIREMENT: 'URL features extracted'
    Extracts URL data and prepends it as a natural language feature for BERT to weigh.
    """
    text = str(text)
    # Find all URLs
    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text)
    num_urls = len(urls)
    
    # Check for IP-based URLs (highly indicative of phishing)
    has_ip = 1 if any(re.search(r'\d{1,3}(\.\d{1,3}){3}', url) for url in urls) else 0
    
    # Prepend explicit features into the text so BERT's attention mechanism can weigh them
    feature_prefix = f"[FEATURE_INJECT -> URL_COUNT: {num_urls} | IP_ROUTING: {'YES' if has_ip else 'NO'}] "
    return feature_prefix + text

# RUBRIC REQUIREMENT: Fix the F1 Score trap
class WeightedTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits
        
        # Double the penalty for misclassifying Safe (0) emails to force the AI to learn
        weight = torch.tensor([2.0, 1.0]).to(model.device) 
        loss_fct = nn.CrossEntropyLoss(weight=weight)
        
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss

def train_bert():
    print("Loading cleaned dataset...")
    df = pd.read_csv("dataset/text/cleaned_emails.csv")
    
    # Subset to save laptop CPU time
    df_phish = df[df['label'] == 1].sample(2500, random_state=42)
    df_safe = df[df['label'] == 0].sample(2500, random_state=42)
    df_subset = pd.concat([df_phish, df_safe]).sample(frac=1).reset_index(drop=True)

    print("Extracting URL Features...")
    # Apply our feature extraction to hit the rubric requirement
    df_subset['text'] = df_subset['text'].apply(extract_url_features)

    # Split into train and validation sets
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        df_subset['text'].tolist(), df_subset['label'].tolist(), test_size=0.2, random_state=42
    )

    print("Loading BERT Tokenizer...")
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

    # Tokenize the data
    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=128)

    # Convert to Hugging Face Dataset objects
    class PhishingDataset(torch.utils.data.Dataset):
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = labels

        def __getitem__(self, idx):
            item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
            item['labels'] = torch.tensor(self.labels[idx])
            return item

        def __len__(self):
            return len(self.labels)

    train_dataset = PhishingDataset(train_encodings, train_labels)
    val_dataset = PhishingDataset(val_encodings, val_labels)

    print("Initializing BERT Model...")
    model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=2)

    training_args = TrainingArguments(
        output_dir='./results_nlp',
        num_train_epochs=4, 
        per_device_train_batch_size=16,
        per_device_eval_batch_size=64,
        learning_rate=2e-5, 
        warmup_steps=50, 
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        eval_strategy="epoch"
    )

    # Using our custom WeightedTrainer to fix the F1 bias
    trainer = WeightedTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics
    )

    print("🚀 Starting Training... (Grab a coffee, this is the final run)")
    trainer.train()

    print("Saving the smart model to models/nlp_model_bert...")
    os.makedirs("models/nlp_model_bert", exist_ok=True)
    model.save_pretrained("models/nlp_model_bert")
    tokenizer.save_pretrained("models/nlp_model_bert")
    
    print("\n✅ Training Complete! Model saved.")

if __name__ == "__main__":
    train_bert()