import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# 🚨 FIX: Point to the exact images folder
image_dir = 'dataset/images'

# 1. Data Augmentation
datagen = ImageDataGenerator(
    rescale=1./255, rotation_range=15, zoom_range=0.1, 
    horizontal_flip=True, validation_split=0.2
)

train_data = datagen.flow_from_directory(
    image_dir, target_size=(224, 224), batch_size=32,
    class_mode='binary', subset='training'
)

val_data = datagen.flow_from_directory(
    image_dir, target_size=(224, 224), batch_size=32,
    class_mode='binary', subset='validation'
)

# 2. Base Model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False 

# 3. Classification Head
x = base_model.output
x = GlobalAveragePooling2D()(x)
predictions = Dense(1, activation='sigmoid')(x)
model = Model(inputs=base_model.input, outputs=predictions)

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='binary_crossentropy', metrics=['accuracy'])

# 4. Class Weights
weights = {0: 0.74, 1: 1.54} 

print("Training Vision Model...")
model.fit(train_data, validation_data=val_data, epochs=10, class_weight=weights)

# 🚨 FIX: Save directly into the models folder
os.makedirs("models", exist_ok=True)
model_path = 'models/vision_model.keras'
model.save(model_path)
print(f"✅ Model saved as {model_path}")