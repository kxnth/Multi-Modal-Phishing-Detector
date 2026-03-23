import numpy as np
import tensorflow as tf
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

print("Loading test data...")
test_data = tf.keras.utils.image_dataset_from_directory(
    'dataset', image_size=(224, 224), batch_size=32, label_mode='binary', shuffle=False
)
model = tf.keras.models.load_model("vision_model.keras")

y_true = np.concatenate([y for x, y in test_data], axis=0)
y_pred = (model.predict(test_data) > 0.5).astype(int)

print("\n--- Vision Model Metrics ---")
print(classification_report(y_true, y_pred))

cm = confusion_matrix(y_true, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Safe', 'Phishing'], yticklabels=['Safe', 'Phishing'])
plt.title("Vision Model Confusion Matrix")
plt.savefig('confusion_matrix.png')
print("Saved confusion_matrix.png for your report.")