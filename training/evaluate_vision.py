import numpy as np
import tensorflow as tf
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("Loading test data...")
# 🚨 FIX: Point to the images folder
test_data = tf.keras.utils.image_dataset_from_directory(
    'dataset/images', image_size=(224, 224), batch_size=32, label_mode='binary', shuffle=False
)

# 🚨 FIX: Load from the models folder
print("Loading vision model...")
model = tf.keras.models.load_model("models/vision_model.keras")

y_true = np.concatenate([y for x, y in test_data], axis=0)
y_pred = (model.predict(test_data) > 0.5).astype(int)

print("\n--- Vision Model Metrics ---")
print(classification_report(y_true, y_pred))

cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Safe', 'Phishing'], yticklabels=['Safe', 'Phishing'])
plt.title("Vision Model Confusion Matrix")

# 🚨 FIX: Save to the results folder
os.makedirs("results", exist_ok=True)
save_path = 'results/confusion_matrix.png'
plt.savefig(save_path)
print(f"✅ Saved {save_path} for your report.")