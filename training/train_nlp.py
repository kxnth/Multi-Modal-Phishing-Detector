import pandas as pd
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

print("Loading dataset...")
df = pd.read_csv("cleaned_emails.csv").dropna()
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
def tokenize_fn(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True, max_length=128)

train_dataset = Dataset.from_pandas(train_df).map(tokenize_fn, batched=True)
test_dataset = Dataset.from_pandas(test_df).map(tokenize_fn, batched=True)

model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=2)

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    return {'accuracy': accuracy_score(labels, preds), 'f1': f1}

training_args = TrainingArguments(
    output_dir='./results', num_train_epochs=3, per_device_train_batch_size=16,
    learning_rate=2e-5, eval_strategy="epoch"
)

trainer = Trainer(model=model, args=training_args, train_dataset=train_dataset,
                  eval_dataset=test_dataset, compute_metrics=compute_metrics)

print("Training BERT...")
trainer.train()

model.save_pretrained("./nlp_model_bert")
tokenizer.save_pretrained("./nlp_model_bert")
print("Saved to ./nlp_model_bert/")