import os
import pandas as pd
import numpy as np
import torch
from sklearn.metrics import classification_report, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def evaluate_nlp():
    print("--- Evaluating NLP Model (BERT) ---")
    # Load Model
    #	
    nlp_path = "ealvaradob/bert-finetuned-phishing"
    tokenizer = DistilBertTokenizer.from_pretrained(nlp_path, local_files_only=True)
    model = DistilBertForSequenceClassification.from_pretrained(nlp_path, local_files_only=True)
    
    # Load a sample of your cleaned test data
    df = pd.read_csv("dataset/text/cleaned_emails.csv").sample(500, random_state=42) # Test on 500 emails
    texts = df['text'].tolist()
    true_labels = df['label'].tolist()
    
    predictions = []
    print("Running BERT predictions (this might take a minute)...")
    for text in texts:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            pred = torch.argmax(outputs.logits, dim=1).item()
            predictions.append(pred)
            
    f1 = f1_score(true_labels, predictions)
    print(f"\n✅ NLP F1 Score: {f1:.4f} (Target: >= 0.88)")
    print("\nClassification Report:")
    print(classification_report(true_labels, predictions, target_names=["Safe", "Phishing"]))
    return f1

def evaluate_vision():
    print("\n--- Evaluating Vision Model (MobileNetV2) ---")
    model = load_model("models/vision_model.keras")
    
    # Create test generator
    test_datagen = ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_directory(
        'dataset/images', # Ensure this has 'safe' and 'phishing' subfolders
        target_size=(224, 224),
        batch_size=32,
        class_mode='binary',
        shuffle=False # MUST be false to match labels correctly
    )
    
    print("Running Vision predictions...")
    preds_raw = model.predict(test_generator)
    predictions = (preds_raw > 0.5).astype(int).flatten()
    true_labels = test_generator.classes
    
    f1 = f1_score(true_labels, predictions)
    print(f"\n✅ Vision F1 Score: {f1:.4f} (Target: >= 0.80)")
    
    # 1. Generate Confusion Matrix (Required for Rubric)
    cm = confusion_matrix(true_labels, predictions)
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Safe', 'Phishing'], yticklabels=['Safe', 'Phishing'])
    plt.title('Vision Model Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig('results/vision_confusion_matrix.png')
    print("✅ Confusion matrix saved to results/vision_confusion_matrix.png")
    
    # 2. Find Misclassified Examples (Required for Rubric)
    print("\n--- Top Misclassified Images (False Positives/Negatives) ---")
    filenames = test_generator.filenames
    misclassified_count = 0
    for i in range(len(true_labels)):
        if true_labels[i] != predictions[i]:
            print(f"File: {filenames[i]} | True: {true_labels[i]} | Predicted: {predictions[i]}")
            misclassified_count += 1
            if misclassified_count >= 10: # Just print 10 so we don't spam the console
                break

if __name__ == "__main__":
    # Make sure results folder exists for the confusion matrix image
    os.makedirs("results", exist_ok=True)
    
    evaluate_nlp()
    evaluate_vision()
    