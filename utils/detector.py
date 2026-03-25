import os
import logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
logging.getLogger('tensorflow').setLevel(logging.ERROR)
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

import torch
import numpy as np
import re
from transformers import BertTokenizer, BertForSequenceClassification

# Load trained models for text and image analysis
nlp_path = "models/nlp_model_bert"
tokenizer = BertTokenizer.from_pretrained(nlp_path)
nlp_model = BertForSequenceClassification.from_pretrained(nlp_path)
nlp_model.eval()

vision_model = load_model("models/vision_model.keras")

# Normalize text to lowercase and count URLs
def clean_text(text):
    text = str(text).lower()
    urls = len(re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text))
    return f"[urls:{urls}] {text}"

def analyze_phishing(combined_text, image_path):
    # Get phishing probability from the text model
    cleaned_text = clean_text(combined_text)
    inputs = tokenizer(cleaned_text, return_tensors="pt", truncation=True, max_length=256, padding=True)
    with torch.no_grad():
        outputs = nlp_model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        nlp_prob = float(probs[0][1].item())

    # Get phishing probability from the image model
    vision_prob = 0.0
    if image_path and os.path.exists(image_path):
        img = load_img(image_path, target_size=(224, 224))
        img_array = img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)
        
        raw_vision = float(vision_model.predict(img_array, verbose=0)[0][0])
        vision_prob = raw_vision ** 2 

    # Merge text and image scores using Bayesian reasoning
    if vision_prob > 0:
        numerator = nlp_prob * vision_prob
        denominator = numerator + ((1 - nlp_prob) * (1 - vision_prob))
        combined_score = numerator / denominator if denominator != 0 else 1.0
    else:
        combined_score = nlp_prob

    # Classify the merged score as PHISHING, SUSPICIOUS, or SAFE
    if combined_score > 0.80:
        verdict = "🚨 PHISHING DETECTED"
    elif combined_score > 0.50:
        verdict = "⚠️ SUSPICIOUS"
    else:
        verdict = "✅ SAFE"
        
    report = f"<strong>NLP:</strong> {nlp_prob*100:.1f}% &nbsp;|&nbsp; <strong>Vision:</strong> {vision_prob*100:.1f}% &nbsp;|&nbsp; <strong>Fusion:</strong> {combined_score*100:.1f}%"
    
    return report, verdict