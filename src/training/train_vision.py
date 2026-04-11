import os
import logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
logging.getLogger('tensorflow').setLevel(logging.ERROR)

import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, RandomBrightness, RandomContrast
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint
import warnings
warnings.filterwarnings("ignore")

def train_vision_model():
    # Load and split images into 80% training and 20% validation sets
    print("Loading screenshot dataset...")
    train_ds = image_dataset_from_directory(
        'data/images', validation_split=0.2, subset="training", 
        seed=42, image_size=(224, 224), batch_size=32, label_mode='binary',
        class_names=['safe', 'phishing']
    )
    val_ds = image_dataset_from_directory(
        'data/images', validation_split=0.2, subset="validation", 
        seed=42, image_size=(224, 224), batch_size=32, label_mode='binary',
        class_names=['safe', 'phishing']
    )

    # Randomly adjust brightness and contrast to help the model focus on patterns, not appearance
    data_augmentation = tf.keras.Sequential([
        RandomBrightness(factor=0.2),
        RandomContrast(factor=0.2),
    ])

    preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input
    
    # Load pre-trained MobileNetV2 and freeze its weights
    print("Building MobileNetV2 Architecture...")
    base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False
    
    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = data_augmentation(inputs) 
    x = preprocess_input(x)       
    x = base_model(x, training=False) 
    
    # Add classification layers to predict safe vs phishing
    x = GlobalAveragePooling2D()(x) 
    x = Dropout(0.2)(x) 
    outputs = Dense(1, activation='sigmoid')(x) 
    
    model = Model(inputs, outputs)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), 
                  loss='binary_crossentropy', metrics=['accuracy'])
    
    # Weight classes to penalize false positives on safe websites
    class_weights = {0: 1.0, 1: 6.0}

    # Train only the new custom decision maker first.
    print("\nPhase 1: Training custom classification head...")
    model.fit(train_ds, validation_data=val_ds, epochs=3, class_weight=class_weights, verbose=1)
    
    # Unlock the deeper layers to fine-tune specific visual details.
    print("\nPhase 2: Fine-tuning deep layers...")
    base_model.trainable = True
    
    for layer in base_model.layers[:100]:
        layer.trainable = False
        
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5), 
                  loss='binary_crossentropy', metrics=['accuracy'])
    
    os.makedirs("models", exist_ok=True)
    checkpoint = ModelCheckpoint("models/vision_model.keras", save_best_only=True, monitor="val_accuracy", mode="max")
    
    model.fit(train_ds, validation_data=val_ds, epochs=5, class_weight=class_weights, callbacks=[checkpoint], verbose=1)
    
    # Save the finished AI model.
    print("\nVision Model saved to models/vision_model.keras!")

if __name__ == "__main__":
    train_vision_model()