import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import pandas as pd
import numpy as np
import torch
import re
from sklearn.metrics import classification_report, f1_score, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import BertTokenizer, BertForSequenceClassification
import warnings
warnings.filterwarnings("ignore")
import logging
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Normalize text to lowercase and count URLs
def clean_text(text):
    text = str(text).lower()
    urls = len(re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text))
    return f"[urls:{urls}] {text}"

def evaluate_nlp():
    # Test the NLP model on held-out test data
    print("--- Evaluating NLP Model ---")
    
    nlp_path = "models/nlp_model_bert"
    if not os.path.exists(nlp_path):
        print("Models not found. Run training first.")
        return

    tokenizer = BertTokenizer.from_pretrained(nlp_path, local_files_only=True)
    model = BertForSequenceClassification.from_pretrained(nlp_path, local_files_only=True)

    test_split_path = "dataset/splits/test_set.csv"
    df_test = pd.read_csv(test_split_path)
    
    df_test['text'] = df_test['text'].apply(clean_text)
    texts = df_test['text'].tolist()
    true_labels = df_test['label'].tolist()
    
    print("Running Model Inference on Test Set...")
    model.eval()
    predictions = []
    
    for text in texts:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            pred = torch.argmax(outputs.logits, dim=1).item()
            predictions.append(pred)

    f1 = f1_score(true_labels, predictions, average='macro')
    print(f"\nNLP Macro F1 Score: {f1:.4f}")
    print("\nClassification Report:")
    print(classification_report(true_labels, predictions, target_names=["Safe", "Phishing"]))
    
    cm = confusion_matrix(true_labels, predictions)
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=["Safe", "Phishing"], yticklabels=["Safe", "Phishing"])
    plt.title("NLP Model Confusion Matrix")
    os.makedirs("results_nlp", exist_ok=True)
    plt.savefig("results_nlp/nlp_confusion_matrix.png")
    plt.close()
    print("NLP Matrix saved.")

def evaluate_vision():
    # Test the vision model on held-out test data
    print("\n--- Evaluating Vision Model ---")
    try:
        import tensorflow as tf
        from tensorflow.keras.models import load_model
        
        test_data = tf.keras.utils.image_dataset_from_directory(
            'dataset/images', 
            image_size=(224, 224), 
            batch_size=32, 
            label_mode='binary', 
            shuffle=False
        )
        
        model = load_model("models/vision_model.keras")
        true_labels = np.concatenate([y for x, y in test_data], axis=0).flatten()
        preds_raw = model.predict(test_data)
        
        predictions = (preds_raw > 0.40).astype(int).flatten()
        
        f1 = f1_score(true_labels, predictions)
        print(f"\nVision F1 Score: {f1:.4f}")
        
        print("\nClassification Report:")
        print(classification_report(true_labels, predictions))
        
        cm = confusion_matrix(true_labels, predictions)
        plt.figure(figsize=(6,5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Safe', 'Phishing'], yticklabels=['Safe', 'Phishing'])
        plt.title('Vision Model Confusion Matrix')
        os.makedirs("results_nlp", exist_ok=True)
        plt.savefig('results_nlp/vision_confusion_matrix.png')
        plt.close()
        print("Vision Matrix saved.")
        
    except Exception as e:
        print(f"Vision evaluation failed: {e}")

if __name__ == "__main__":
    evaluate_nlp()
    evaluate_vision()