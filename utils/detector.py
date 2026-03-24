import os
import numpy as np
import torch
import torch.nn.functional as F
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Load Models
nlp_path = "models/nlp_model_bert"
tokenizer = DistilBertTokenizer.from_pretrained(nlp_path, local_files_only=True)
nlp_model = DistilBertForSequenceClassification.from_pretrained(nlp_path, local_files_only=True)
vision_model = load_model("models/vision_model.keras")

def analyze_phishing(combined_text, image_path):
    # 1. NLP Score
    inputs = tokenizer(combined_text, return_tensors="pt", truncation=True, max_length=128, padding=True)
    with torch.no_grad():
        outputs = nlp_model(**inputs)
        nlp_prob = F.softmax(outputs.logits, dim=-1)[0][1].item()

    # 2. Vision Score (Only if an image exists)
    vision_prob = 0.0
    if image_path and os.path.exists(image_path):
        img = load_img(image_path, target_size=(224, 224))
        img_array = img_to_array(img) / 255.0  
        img_array = np.expand_dims(img_array, axis=0)
        vision_prob = float(vision_model.predict(img_array, verbose=0)[0][0])
        
        # 3. Multi-Modal Fusion (Rubric: Smart Ensemble Method)
        weight_nlp = 0.60
        weight_vision = 0.40
        combined_score = (nlp_prob * weight_nlp) + (vision_prob * weight_vision)
        
        # VETO RULE: If one model is highly confident it's an attack, trust it over the average.
        if vision_prob > 0.85:
            combined_score = max(combined_score, vision_prob)
        elif nlp_prob > 0.85:
            combined_score = max(combined_score, nlp_prob)
            
    else:
        # If no URL was provided (just an email), rely 100% on NLP
        combined_score = nlp_prob

    # 4. Final Verdict Logic
    if combined_score > 0.70:
        verdict = "🚨 PHISHING DETECTED"
    elif combined_score > 0.40:
        verdict = "⚠️ SUSPICIOUS"
    else:
        verdict = "✅ SAFE"
        
    report = f"**NLP:** {nlp_prob*100:.1f}% | **Vision:** {vision_prob*100:.1f}% | **Fusion:** {combined_score*100:.1f}%"
    return report, verdict