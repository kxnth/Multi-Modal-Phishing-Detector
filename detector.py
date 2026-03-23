import os
import numpy as np
import torch
import torch.nn.functional as F
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# 1. Load Models Globally
model_path = os.path.abspath("nlp_model_bert")
tokenizer = DistilBertTokenizer.from_pretrained(model_path, local_files_only=True)
nlp_model = DistilBertForSequenceClassification.from_pretrained(model_path, local_files_only=True)
vision_model = load_model("vision_model.keras")

def analyze_phishing(email_text, image_path):
    # 2. NLP Score (BERT)
    inputs = tokenizer(email_text, return_tensors="pt", truncation=True, max_length=128, padding=True)
    with torch.no_grad():
        outputs = nlp_model(**inputs)
        nlp_prob = F.softmax(outputs.logits, dim=-1)[0][1].item()

    # 3. Vision Score (MobileNetV2)
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0  
    img_array = np.expand_dims(img_array, axis=0)
    vision_prob = float(vision_model.predict(img_array, verbose=0)[0][0])

    # 4. Fusion Math (80% Text / 20% Vision)
    combined_score = (nlp_prob * 0.80) + (vision_prob * 0.20)
    
    # 5. Final Verdict Logic
    if combined_score > 0.85:
        verdict = "🚨 PHISHING DETECTED"
    elif combined_score > 0.50:
        verdict = "⚠️ SUSPICIOUS"
    else:
        verdict = "✅ SAFE"
        
    report = f"**NLP:** {nlp_prob*100:.1f}% | **Vision:** {vision_prob*100:.1f}% | **Fusion:** {combined_score*100:.1f}%"
    return report, verdict